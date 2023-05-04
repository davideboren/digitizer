#ifndef _MONSTER_DEFS_H_
#define _MONSTER_DEFS_H_

#include <Arduino.h>

enum MonsterName {
    Tyrannomon,
    Yukimibotamon
};

struct MonsterRef {
    String filename;
};

static const MonsterRef MonsterDB[] = {
    {"sprite/adult/Tyrannomon.bmp"},
    {"sprite/baby/Yukimibotamon.bmp"},
};
#endif //_MONSTER_DEFS_H_