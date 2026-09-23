#pragma once
inline bool configEnabled=true;
struct Config {template<class T>T GetOption(char const*,T){return T(configEnabled);}};
inline Config config;
inline Config* sConfigMgr=&config;
