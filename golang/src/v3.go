package main

// 更好的解析和处理。

import (
	"fmt"
	"net"
	"encoding/binary"
	"bytes"
	"errors"
	"strings"
	"time"
)

const (
	BufferSize  = 1024
	ServerAddr  = "openbarrage.douyutv.com:8601"
	PostCode = 689
	PullCode = 690
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


func PreParse(conn net.Conn) (string, error){
	var header = make([]byte, 12)
	var buffer = make([]byte, BufferSize)
	//var msgLen  int32
	_, err := conn.Read(header)
	if err != nil{
		return "", errors.New("预解析失败")
	}
	conn.Read(buffer)
	return string(buffer), nil
}


func ParseData(conn net.Conn) map[string]interface{} {
	// 解析， 将二进制数据转化为可读的
	Parsed := make(map[string]interface{})
	str, err := PreParse(conn)
	if err != nil{
		fmt.Println(err)
	}

	s := strings.Trim(str, "/")
	items := strings.Split(s, "/")
	for _, str := range items {
		k := strings.SplitN(str, "@=", 2)
		if len(k) >1{
			Parsed[k[0]] = k[1]
		}
	}
	return Parsed
}

func PreConn(roomid string) net.Conn  {
	buffer := make([]byte, BufferSize)
	JoinData := JoinRoom(roomid)
	JoinMsg := JoinMsg(roomid)
	conn, _ := net.Dial("tcp", ServerAddr)
	_, werr := conn.Write(JoinData)
	if werr != nil{
		fmt.Println(werr)
	}
	_, err := conn.Read(buffer)
	if err != nil {
		fmt.Println(errors.New("无法连接房间 " + err.Error()))
	}
	conn.Write(JoinMsg)
	return conn
}


func Connect()  {
	//buffer := make([]byte, BufferSize)
	conn := PreConn("606118")
	timestamp := time.Now().Unix()
	for  {
		parsed := ParseData(conn) // type: dgb - gift, chatmsg - danmu , uenter - enter
		// nn - nickname  level  txt
		if time.Now().Unix() - timestamp > 21{
			timestamp = time.Now().Unix()
			_, err := conn.Write(PostData(fmt.Sprintf("type@=keeplive/tick@=%s/", timestamp)))
			if err != nil{
				fmt.Println("心跳失败")
			}
		}
		if parsed["type"] == "chatmsg"{
			fmt.Printf("user: %s  danmu: %s level: %s \n", parsed["nn"], parsed["txt"], parsed["level"])
		}

	}
	conn.Close()
}



func main()  {
	Connect()
}


