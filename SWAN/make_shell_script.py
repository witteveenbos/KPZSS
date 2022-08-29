# -*- coding: utf-8 -*-
"""
Created on Thu Aug  4 14:20:41 2022

@author: ENGT2
"""

from hmtoolbox.WB_putty import run_all_qsub_shell

path = r'z:\130991_Systeemanalyse_ZSS\3.Models\SWAN\1D\Westerschelde\tests\test_04_wind_perp';

run_all_qsub_shell.create_shell_script(path)