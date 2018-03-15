package base

import (
	"time"
	"strconv"
)

// 获取 int 时间戳
func timeStamp() int {
	t := time.Now()
	timestamp := strconv.FormatInt(t.UTC().UnixNano(), 10)[:10]
	tt,_ := strconv.Atoi(timestamp)
	return tt
}
