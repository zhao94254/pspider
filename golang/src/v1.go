package main

import (
"fmt"
"net"
"encoding/binary"
"bytes"
"errors"
"strings"
)

const (
	BufferSize  = 1024
	ServerAddr  = "openbarrage.douyutv.com:8601"
	PostCode = 689
	PullCode = 690
	Roomid = 688
)

func PostData(msg string) []byte {
	// 构造需要发送的二进制数据
	length := 9+len(msg) // 长度4字节 + 类型2字节 + 加密字段1字节 + 保留字段1字节 + 结尾字段1字节
	buffer := bytes.NewBuffer([]byte{})
	binary.Write(buffer, binary.LittleEndian, int32(length))
	binary.Write(buffer, binary.LittleEndian, int32(length))
	binary.Write(buffer, binary.LittleEndian, int16(PostCode))
	binary.Write(buffer, binary.LittleEndian, int8( 0))
	binary.Write(buffer, binary.LittleEndian, int8(0))
	binary.Write(buffer, binary.LittleEndian, []byte(msg))
	binary.Write(buffer, binary.LittleEndian, int8(0))
	fmt.Println(buffer)
	return buffer.Bytes()
}

func JoinRoom(roomid string)[]byte  {
	// 选择要链接的房间号
	msg := fmt.Sprintf("type@=loginreq/roomid@=%s/", roomid)
	return PostData(msg)
}

func JoinMsg(roomid string)[]byte{
	msg := fmt.Sprintf("type@=joingroup/rid@=%s/gid@=-9999/", roomid)
	return PostData(msg)
}

func ParseData(buffer []byte) map[string]interface{} {
	// 解析， 将二进制数据转化为可读的
	Parsed := make(map[string]interface{})
	s := strings.Trim(string(buffer), "/")
	items := strings.Split(s, "/")
	for _, str := range items {
		k := strings.SplitN(str, "@=", 2)
		if len(k) >1{
			Parsed[k[0]] = k[1]
		}
	}
	return Parsed
}

func Connect()  {
	buffer := make([]byte, BufferSize)
	JoinData := JoinRoom("688")
	JoinMsg := JoinMsg("688")
	conn, _ := net.Dial("tcp", ServerAddr)
	fmt.Println(JoinData)
	_, werr := conn.Write(JoinData)
	if werr != nil{
		fmt.Println(werr)
	}
	_, err := conn.Read(buffer)
	if err != nil {
		fmt.Println(errors.New("无法连接房间 " + err.Error()))
	}
	conn.Write(JoinMsg)
	for  {
		_, err := conn.Read(buffer)
		parsed := ParseData(buffer)
		fmt.Println(parsed["level"],parsed["nn"], parsed["txt"])
		if err != nil{
			break
		}
	}
	conn.Close()
}



func main()  {
	Connect()
}


