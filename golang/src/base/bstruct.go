package base

import "sync"

type SafeMap struct {
	sync.RWMutex
	Map map[string]int
}

func (sm *SafeMap) readMap(key string) int {
	sm.RLock()
	value := sm.Map[key]
	sm.RUnlock()
	return value
}

func (sm *SafeMap) writeMap(key string,) {
	sm.Lock()
	sm.Map[key]++
	sm.Unlock()
}

