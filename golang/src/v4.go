package main

import (
	"asyncrawl/golang/src/base"
)

func test()  {
	ch := make(chan string)
	rooms := base.Pindao()
	for _, i := range rooms{
		go base.Connect(i)
	}
	for i:=1;i<len(rooms) ;i++  {
		<-ch
	}
}
// todo fix bug。


func main()  {
	test()
}
