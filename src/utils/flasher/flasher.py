import re
from ..kboot.build.ktool import KTool
from .base_flasher import BaseFlasher

class Flasher(BaseFlasher):
    """
    A class to parse KTool outputs
    
    We don't want to modify the KTool structure,
    instead, only parse what happens in :attr:`KTool.process`.
    
    So, we need to overwrite the :attr:`KTool.print_callback`
    and parses its outputs to pipe them to krux-installer UI
    """
    def __init__(self, device: str, on_log: typing.Callable):
        super().__init__(device=device, on_log=on_log)

        def print_callback(*args, **kwargs):
            
            # Parses output when `KTool.process.printProgressBar` is called` (line 427)
            if kwargs.get("end") and kwargs.get("end") == '\r':
                info = " ".join(*args)
                info += kwargs.get("end")
                data = args.split("|")
                prefix = data[0].replace(" ", "")
                percent = data[2]
                suffix = data[3]
                self.info(f"{prefix} | {percent} | {suffix}")
                self.on_log(*(prefix, percent, suffix))

            # Parses output when `KTool.process.ISPResponse.parse` ValueError is raised (line 512)
            elif re.findall(args[0], "Warning: recv unknown op"):
                self.info(": ".join(args))
                self.on_log(*args)

            # Parses output when `KTool.process.MAIXLoader.change_baudrate` is called (line 667)
            elif re.findall(args[1], "Selected Baudrate"):
                self.info(": ".join(args[1:3])
                self.on_log(*args[1:3])

            # Parses output when `KTool.process.MAIXLoader.change_baudrate` is called
            # with args.Board == "goE" with baudrate > 4500000
            re.findall(args[1], "Enable OPENEC super baudrate!!!"):
                self.warn(args[1])
                self.on_log(args[1])
                
            # TODO: do more parses
            else:
                self.info()
        
        KTool.print_callback = print_callback

    

