START TRANSACTION;
DELETE FROM spell_script_names WHERE spell_id=760056 AND ScriptName='spell_hero_grapple';
DELETE FROM spell_script_names WHERE spell_id=760094 AND ScriptName='spell_hero_grapple';
DELETE FROM spell_script_names WHERE spell_id=760096 AND ScriptName='aura_hero_grapple_window';
COMMIT;
