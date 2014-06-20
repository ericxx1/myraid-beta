New Socket("Test"):
    Test.connect("127.0.0.1", 5675)
    test.recv(4096)
    test.send("hello world")
    var x = 1
    var y = 2
    if(x > y)
        _os.exec("poop")
end
dstack()
