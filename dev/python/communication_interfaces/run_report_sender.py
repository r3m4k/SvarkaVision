# System imports

# External imports

# User imports
from .report_sender import ReportSender
from .Interfaces import CAN, RS485, TCPServer, TCPClient

##########################################################

def run_report_sender():
    interfaces = [RS485(), CAN(), TCPServer(), TCPClient()]
    report_sender = ReportSender(interfaces)

    report_sender.send_report()
