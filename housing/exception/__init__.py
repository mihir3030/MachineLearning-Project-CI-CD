# this file is use for create own Exception handling
import os 
import sys

""" create own Exception class
in construction "error_messsage" is actual error message object of exception
in error details with sys you'll get error details ex. which line causing error
"""
class HousingException(Exception):

    def __init__(self, error_message:Exception, error_detail:sys):
        super().__init__(error_message)  # error message pass to Exception class ex.. Exception(error_message)
        self.error_message = HousingException.detailed_error_message(error_message = error_message, 
                                                                    error_detail = error_detail)
    @staticmethod
    def detailed_error_message(error_message:Exception, error_detail:sys) -> str:
        _,_, exec_tb = error_detail.exc_info()
        
        line_number = exec_tb.tb_frame.f_lineno
        file_name = exec_tb.tb_frame.f_code.co_filename

        error_message = f"Error occured in  scrip: [{file_name}] at line number: [{line_number}]  error_message: [{error_message}] "
        return error_message

    def __str__(self):
        return self.error_message

    def __repr__(self) -> str:
        return HousingException.__name__.str()