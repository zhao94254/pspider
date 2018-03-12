package main

import (
	"./base"
)

func newSafe() *base.SafeMap {
	sm := new(base.SafeMap)
	sm.Map = make(map[string]int)
	return sm
}


func test()  {
	ch := make(chan string)
	count := newSafe()
	rooms := base.Pindao(10)
	for _, i := range rooms{
		go base.CountConnect(i, count)
	}
	for i:=1;i<len(rooms) ;i++  {
		<-ch
	}
}
// todo fix bug。


func main()  {
	test()
}
