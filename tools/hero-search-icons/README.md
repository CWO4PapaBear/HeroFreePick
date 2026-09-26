# Compact advancement search results

Incremental client overlay after hero-menu-preload; enforce manifest before hash. Results use 34px icons at 40px spacing, dynamically wrapping to viewport width. No per-result names or rank text. Existing level/name/ID sorting and search filters are unchanged. Bottom-right class badge uses original entry class. Both ability and talent results use the shared tooltip and pending-click handlers, including Shift-expanded tooltip behavior. Existing overview pooling is reused and hidden through Refresh.

Lua 5.1 and mocked wrapping/order/badge/tooltip/click checks pass. Installed locally with backup; visual acceptance pending. No server changes. Launcher publication remains pending.
