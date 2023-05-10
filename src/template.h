#ifndef _MONSTER_DEFS_H_
#define _MONSTER_DEFS_H_

#include <Arduino.h>

enum MonsterName {
Empty,
out_monster_names
};

enum MonsterStage {
	digitama,
    baby,
    baby_ii,
    child,
    adult,
    perfect,
    ultimate,
    armor
};

struct MonsterRef {
out_monster_ref_struct
};

static const MonsterRef MonsterDB[] = {
{"null", {Kera_Digitama}},
out_monster_refs
};
#endif //_MONSTER_DEFS_H_