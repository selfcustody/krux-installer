def parser(debug, callback: typing.Callable, *args, **kwargs):
    # Parses output when :attr:`KTool.process.printProgressBar is called`
    if kwargs.get("end") and kwargs.get("end") == '\r':
        info = " ".join(*args)
        info += kwargs.get("end")
        data = args.split("|")
        prefix = data[0].replace(" ", "")
        percent = data[2]
        suffix = data[3]
        new_args = (prefix, percent, suffix)
        callback(*new_args)

    # Parses output when :attr:`KTool.process.ISPResponse.parse` is called
    elif args[0] == "Warning: recv unknown op":
        msg = args[0]
        op = args[1]
        new_args = (msg, op)
        callback(*new_args)

    # Parses output when :attr:`KTool.process.MAIXLoader.change_baudrate` is called
    elif args[1] == "Selected Baudrate:":
        msg = args[1]
        baudrate = args[2]
        new_args = (msg, baudrate)
        callback(*new_args)
    
    # Parses output when :attr:`KTool.process.MAIXLoader.change_baudrate` is called and
    # Board is `goE` and its baudrte exceeds 4500000
    elif args[1] == "Enable OPNEC super baudrate!!!":
        msg = args[1]
        new_args = (msg)
        callback(*new_args)
            
    # Parses output when :attr:`KTool.process.MAIXLoader.__init__
    elif args[1] == "Default baudrate is:":
        msg = args[1]
        baudrate = args[2]
        warn = args[3]
        new_args = (msg, baudrate, warn)
        callback(*new_args)

    # Parses output when KTool.process.MAIXLoader.flash_greeting raise an Exception
    elif re.findall(args[1], r"\w+ Error, retrying..."):
        msg = args[1]
        new_args = (msg)
        callback(*new_args)

    # Parses output when KTool.process.MAIXLoader.flash_green
    elif args[1] = "2nd stage ISP ok":
        msg = args[1]
        new_args = (msg)
        callback(*new_args)

    if re.findall(args[1], r"Starting 2nd stage isp at .*"):
        msg = args[1]
        new_args = (msg)
        callback(*new_args)
    
    if args[0] == "Failed, retry":
        msg = args[0]
        new_args = (msg)
        callback(*new_args)
    
    if re.findall(args[1], r"Initialize K210 SPI Flash"):
        msg = args[1]
        new_args = (msg)
        callback(*new_args)
    
    if re.findall(args[1], r"Flash initialized successfully"):
        msg = args[1]
        new_args = (msg)
        callback(*new_args)
    
    if re.findall(args[1], r"Unexcepted Return received, retrying..."):
        msg = args[1]
        new_args = (msg)
        callback(*new_args)

    if re.findall(args[1], r"ISP loaded in \d+\.\d+"):
        msg = args[1]
        new_args = (msg)
        callback(*new_args)
    
    if re.findall(args[1], r"Error Count Exceeed, Stop Trying"):
        msg = args[1]
        new_args = (msg)
        callback(*new_args)
        
    if re.findall(args[1], r"Swapping endianess"):
        msg = args[1]
        new_args = (msg)
        callback(*new_args)
    
    debug(" ".join(new_args))
