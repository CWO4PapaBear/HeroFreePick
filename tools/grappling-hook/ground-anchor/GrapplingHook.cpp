// Original Bear Cave implementation. CoA's temporary replacement design informed
// the packet/cast-routing approach; no generic Ascension aura-337 support is added.
#include "HeroGrapplingHooks.h"
#include "Player.h"
#include "PlayerScript.h"
#include "WorldScript.h"
#include "ScriptMgr.h"
#include "SpellScript.h"
#include "SpellInfo.h"
#include "SpellMgr.h"
#include "SpellAuras.h"
#include "MotionMaster.h"
#include "PathGenerator.h"
#include "WorldPacket.h"
#include "WorldSession.h"
#include "Opcodes.h"
#include "Log.h"
#include "TemporarySummon.h"
#include "ObjectMgr.h"
#include "DatabaseEnv.h"
#include <cmath>
#include <memory>
#include <algorithm>

extern bool HeroClassPlusOwnsSpell(Player*, uint32);

namespace HeroGrapple
{
constexpr uint32 Main = 760056;
constexpr uint32 Follow = 760094;
constexpr uint32 Root = 760095;
constexpr uint32 Window = 760096;
constexpr uint32 Tether = 760058;
constexpr float Speed = 25.0f;
bool Ready = false;

bool Authorized(Player* player)
{
    return Ready && player && player->IsAlive() && player->IsInWorld() &&
        player->HasActiveSpell(Main) && HeroClassPlusOwnsSpell(player, Main);
}

void Swap(Player* player, uint32 from, uint32 to)
{
    if (!player->IsInWorld())
        return;
    WorldPacket packet(SMSG_SUPERCEDED_SPELL, 8);
    packet << from << to;
    player->SendDirectMessage(&packet);
}

uint32 Route(Player* player, uint32 spell)
{
    return spell == Main && Authorized(player) && player->HasAura(Window) &&
        player->HasActiveSpell(Follow) ? Follow : spell;
}

uint32 Persist(Player* player, uint32 spell)
{
    // The temporary replacement is never written into saved action buttons.
    return spell == Follow && player->HasSpell(Main) ? Main : spell;
}

SpellCastResult MovementCheck(Player* player)
{
    if (!Authorized(player))
        return SPELL_FAILED_SPELL_UNAVAILABLE;
    if (player->IsInFlight() || player->IsFalling() || player->GetTransport() ||
        player->GetVehicle() || player->IsMounted() || player->IsInWater())
        return SPELL_FAILED_NOT_HERE;
    if (player->HasUnitState(UNIT_STATE_ROOT | UNIT_STATE_STUNNED | UNIT_STATE_CONFUSED |
        UNIT_STATE_FLEEING) || player->HasUnitFlag(UNIT_FLAG_DISABLE_MOVE))
        return SPELL_FAILED_ROOTED;
    if (player->GetMotionMaster()->GetMotionSlotType(MOTION_SLOT_CONTROLLED) != NULL_MOTION_TYPE)
        return SPELL_FAILED_NOT_READY;
    return SPELL_CAST_OK;
}

SpellCastResult BuildPath(Player* player, Position const& dest, float range,
    std::unique_ptr<PathGenerator>& path, Unit const* target = nullptr)
{
    auto result = MovementCheck(player);
    if (result != SPELL_CAST_OK)
        return result;
    float x = dest.GetPositionX(), y = dest.GetPositionY(), z = dest.GetPositionZ();
    if (!std::isfinite(x) || !std::isfinite(y) || !std::isfinite(z))
        return SPELL_FAILED_BAD_TARGETS;
    if (player->GetExactDist(x, y, z) > range)
        return SPELL_FAILED_OUT_OF_RANGE;
    if (!player->IsWithinLOS(x, y, z))
        return SPELL_FAILED_LINE_OF_SIGHT;
    path = std::make_unique<PathGenerator>(player);
    // The core converts this limit to floor(distance / 4) points. A 15-yard
    // follow-up budget became only three points, rejecting ordinary short paths.
    // Reserve endpoint/rounding slots, then enforce the geometric length below.
    float maxLength = range * 1.5f + (target ? target->GetCombatReach() : 0.0f);
    path->SetPathLengthLimit(maxLength + 2.0f * SMOOTH_PATH_STEP_SIZE);
    if (!path->CalculatePath(x, y, z, false) || path->GetPath().size() < 2 ||
        (path->GetPathType() & (PATHFIND_SHORTCUT | PATHFIND_INCOMPLETE | PATHFIND_NOPATH |
            PATHFIND_NOT_USING_PATH | PATHFIND_SHORT)))
        return SPELL_FAILED_NOPATH;
    auto const& points = path->GetPath();
    float length = 0.0f;
    for (std::size_t i = 1; i < points.size(); ++i)
        length += (points[i] - points[i - 1]).length();
    if (length > maxLength)
        return SPELL_FAILED_NOPATH;
    auto end = path->GetActualEndPosition();
    if (target)
    {
        // Creature origin height can differ from its walkable ground surface.
        // Match the core charge height check, then require a reachable endpoint.
        if (path->IsInvalidDestinationZ(target) || std::fabs(end.z - z) > 5.0f ||
            std::hypot(end.x - x, end.y - y) > std::max(1.0f, target->GetCombatReach()))
            return SPELL_FAILED_NOPATH;
    }
    else if ((path->GetPathType() & PATHFIND_FARFROMPOLY) ||
        std::fabs(end.z - z) > 1.0f || std::hypot(end.x - x, end.y - y) > 1.0f)
        return SPELL_FAILED_NOPATH;
    return SPELL_CAST_OK;
}

class spell_hero_grapple : public SpellScript
{
    PrepareSpellScript(spell_hero_grapple);
    std::unique_ptr<PathGenerator> path;
    bool Validate(SpellInfo const*) override { return ValidateSpellInfo({Main, Follow, Root, Window, Tether}); }
    SpellCastResult Check()
    {
        auto player = GetCaster()->ToPlayer();
        if (!player)
            return SPELL_FAILED_BAD_TARGETS;
        if (GetSpellInfo()->Id == Main)
        {
            if (player->HasAura(Window))
                return SPELL_FAILED_NOT_READY;
            auto dest = GetExplTargetDest();
            return dest ? BuildPath(player, *dest, 30.0f, path) : SPELL_FAILED_BAD_TARGETS;
        }
        if (!player->HasAura(Window))
            return SPELL_FAILED_NOT_READY;
        auto target = GetExplTargetUnit();
        if (!target || !target->IsAlive() || !player->IsValidAttackTarget(target) ||
            !player->InSamePhase(target) || target->GetTransport() || target->GetVehicle())
            return SPELL_FAILED_BAD_TARGETS;
        if (!player->IsWithinLOSInMap(target))
            return SPELL_FAILED_LINE_OF_SIGHT;
        auto result = BuildPath(player, *target, 10.0f, path, target);
        if (result == SPELL_CAST_OK)
            path->ShortenPathUntilDist(G3D::Vector3(target->GetPositionX(),
                target->GetPositionY(), target->GetPositionZ()), std::max(1.0f, target->GetCombatReach()));
        return result;
    }
    void Launch(SpellEffIndex)
    {
        PreventHitDefaultEffect(EFFECT_0);
        if (!path)
            return;
        auto player = GetCaster()->ToPlayer();
        if (!player || MovementCheck(player) != SPELL_CAST_OK)
            return;
        // The validated path is used directly; no teleport or path-failure fallback.
        if (GetSpellInfo()->Id == Main)
        {
            if (auto dest = GetExplTargetDest())
                if (auto anchor = player->SummonCreature(18721, *dest, TEMPSUMMON_TIMED_DESPAWN, 2000))
                {
                    // This helper exists only to anchor the ground-cast visual.
                    // Reduce its model attachment height to near ground level,
                    // without moving the cast point or changing enemy models.
                    anchor->SetObjectScale(0.01f);
                    player->CastSpell(anchor, Tether, true);
                }
            player->CastSpell(player, Window, true);
        }
        else
        {
            player->RemoveAurasDueToSpell(Window);
            if (auto target = GetExplTargetUnit())
            {
                player->CastSpell(target, Tether, true);
                player->CastSpell(target, Root, true);
            }
        }
        player->GetMotionMaster()->MoveCharge(*path, Speed);
    }
    void Register() override
    {
        OnCheckCast += SpellCheckCastFn(spell_hero_grapple::Check);
        OnEffectHit += SpellEffectFn(spell_hero_grapple::Launch, EFFECT_0, SPELL_EFFECT_DUMMY);
    }
};

class aura_hero_grapple_window : public AuraScript
{
    PrepareAuraScript(aura_hero_grapple_window);
    void Apply(AuraEffect const*, AuraEffectHandleModes)
    {
        auto player = GetTarget()->ToPlayer();
        if (!Authorized(player))
            return;
        player->_addSpell(Follow, SPEC_MASK_ALL, true);
        if (player->HasActiveSpell(Follow))
            Swap(player, Main, Follow);
    }
    void Remove(AuraEffect const*, AuraEffectHandleModes)
    {
        if (auto player = GetTarget()->ToPlayer())
        {
            if (player->HasSpell(Main))
                Swap(player, Follow, Main);
            player->removeSpell(Follow, SPEC_MASK_ALL, true);
        }
    }
    void Register() override
    {
        AfterEffectApply += AuraEffectApplyFn(aura_hero_grapple_window::Apply,
            EFFECT_0, SPELL_AURA_DUMMY, AURA_EFFECT_HANDLE_REAL);
        AfterEffectRemove += AuraEffectRemoveFn(aura_hero_grapple_window::Remove,
            EFFECT_0, SPELL_AURA_DUMMY, AURA_EFFECT_HANDLE_REAL);
    }
};

class Lifecycle final : public PlayerScript
{
public:
    Lifecycle() : PlayerScript("HeroGrappleLifecycle", {PLAYERHOOK_ON_LOGIN,
        PLAYERHOOK_ON_BEFORE_LOGOUT, PLAYERHOOK_ON_UPDATE, PLAYERHOOK_ON_FORGOT_SPELL}) { }
    void OnPlayerLogin(Player* player) override
    {
        player->RemoveAurasDueToSpell(Window);
        player->removeSpell(Follow, SPEC_MASK_ALL, true);
    }
    void OnPlayerBeforeLogout(Player* player) override { player->RemoveAurasDueToSpell(Window); }
    void OnPlayerForgotSpell(Player* player, uint32 spell) override
    {
        if (spell == Main)
            player->RemoveAurasDueToSpell(Window);
    }
    void OnPlayerUpdate(Player* player, uint32) override
    {
        // Build ownership is checked at cast time, not by polling SQL each tick.
        // Build removal also invokes OnPlayerForgotSpell.
        if (player->HasAura(Window) && (!player->IsAlive() || !player->HasActiveSpell(Main)))
            player->RemoveAurasDueToSpell(Window);
    }
};

class Startup final : public WorldScript
{
public:
    Startup() : WorldScript("HeroGrappleStartup", {WORLDHOOK_ON_STARTUP}) { }
    void OnStartup() override
    {
        Ready = false;
        auto window = const_cast<SpellInfo*>(sSpellMgr->GetSpellInfo(Window));
        if (!window || !sSpellMgr->GetSpellInfo(Main) || !sSpellMgr->GetSpellInfo(Follow) ||
            !sSpellMgr->GetSpellInfo(Root) || !sSpellMgr->GetSpellInfo(Tether) ||
            !sObjectMgr->GetCreatureTemplate(18721) ||
            window->Effects[EFFECT_0].ApplyAuraName != SPELL_AURA_DUMMY)
        {
            LOG_ERROR("server.loading", "HERO_GRAPPLE validation failed: matching spell data required");
            return;
        }
        auto bindings = WorldDatabase.Query("SELECT COUNT(*) FROM spell_script_names WHERE "
            "(spell_id IN (760056,760094) AND ScriptName='spell_hero_grapple') OR "
            "(spell_id=760096 AND ScriptName='aura_hero_grapple_window')");
        if (!bindings || bindings->Fetch()[0].Get<uint64>() != 3)
        {
            LOG_ERROR("server.loading", "HERO_GRAPPLE validation failed: script bindings missing");
            return;
        }
        window->AttributesCu |= SPELL_ATTR0_CU_AURA_CANNOT_BE_SAVED;
        Ready = true;
        LOG_INFO("server.loading", "HERO_GRAPPLE ready v1; scoped temporary follow-up; Classic unchanged");
    }
};
}

void AddHeroGrapplingScripts()
{
    using namespace HeroGrapple;
    HeroGrapplingHooks::CastResolver() = HeroGrapple::Route;
    HeroGrapplingHooks::ActionResolver() = HeroGrapple::Persist;
    RegisterSpellScript(spell_hero_grapple);
    RegisterSpellScript(aura_hero_grapple_window);
    new HeroGrapple::Lifecycle();
    new HeroGrapple::Startup();
}
