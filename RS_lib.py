# -*- coding: utf-8 -*-
"""
Created on Tue Jul 18 14:03:48 2023

@author: cold
"""

from typing import Any

import qcodes.validators as vals
from qcodes.instrument import VisaInstrument
from qcodes.parameters import create_on_off_val_mapping


class RohdeSchwarzSGS100A(VisaInstrument):
    """
    This is the QCoDeS driver for the Rohde & Schwarz SGS100A signal generator.

    Status: beta-version.

    .. todo::

        - Add all parameters that are in the manual
        - Add test suite
        - See if there can be a common driver for RS mw sources from which
          different models inherit

    This driver will most likely work for multiple Rohde & Schwarz sources.
    it would be a good idea to group all similar RS drivers together in one
    module.

    Tested working with

    - RS_SGS100A

    This driver does not contain all commands available for the RS_SGS100A but
    only the ones most commonly used.
    """

    def __init__(self, name: str, address: str, **kwargs: Any) -> None:
        super().__init__(name, address, terminator='\n', **kwargs)

        self.add_parameter(name='frequency',
                           label='Frequency',
                           unit='Hz',
                           get_cmd='SOUR:FREQ?',
                           set_cmd='SOUR:FREQ {:.2f}',
                           get_parser=float,
                           vals=vals.Numbers(1e6, 20e9))
        self.add_parameter(name='phase',
                           label='Phase',
                           unit='deg',
                           get_cmd='SOUR:PHAS?',
                           set_cmd='SOUR:PHAS {:.2f}',
                           get_parser=float,
                           vals=vals.Numbers(0, 360))
        self.add_parameter(name='power',
                           label='Power',
                           unit='dBm',
                           get_cmd='SOUR:POW?',
                           set_cmd='SOUR:POW {:.2f}',
                           get_parser=float,
                           vals=vals.Numbers(-120, 25))
        self.add_parameter('status',
                           label='RF Output',
                           get_cmd=':OUTP:STAT?',
                           set_cmd=':OUTP:STAT {}',
                           val_mapping=create_on_off_val_mapping(on_val='1',
                                                                 off_val='0'))
        self.add_parameter('IQ_state',
                           label='IQ Modulation',
                           get_cmd=':IQ:STAT?',
                           set_cmd=':IQ:STAT {}',
                           val_mapping=create_on_off_val_mapping(on_val='1',
                                                                 off_val='0'))
        self.add_parameter('pulsemod_state',
                           label='Pulse Modulation',
                           get_cmd=':SOUR:PULM:STAT?',
                           set_cmd=':SOUR:PULM:STAT {}',
                           val_mapping=create_on_off_val_mapping(on_val='1',
                                                                 off_val='0'))
        self.add_parameter('pulsemod_source',
                           label='Pulse Modulation Source',
                           get_cmd='SOUR:PULM:SOUR?',
                           set_cmd='SOUR:PULM:SOUR {}',
                           vals=vals.Enum('INT', 'EXT', 'int', 'ext'))
        self.add_parameter('ref_osc_source',
                           label='Reference Oscillator Source',
                           get_cmd='SOUR:ROSC:SOUR?',
                           set_cmd='SOUR:ROSC:SOUR {}',
                           vals=vals.Enum('INT', 'EXT', 'int', 'ext'))
        # Define LO source INT/EXT (Only with K-90 option)
        self.add_parameter('LO_source',
                           label='Local Oscillator Source',
                           get_cmd='SOUR:LOSC:SOUR?',
                           set_cmd='SOUR:LOSC:SOUR {}',
                           vals=vals.Enum('INT', 'EXT', 'int', 'ext'))
        # Define output at REF/LO Output (Only with K-90 option)
        self.add_parameter('ref_LO_out',
                           label='REF/LO Output',
                           get_cmd='CONN:REFL:OUTP?',
                           set_cmd='CONN:REFL:OUTP {}',
                           vals=vals.Enum('REF', 'LO', 'OFF', 'ref', 'lo',
                                          'off', 'Off'))
        # Frequency mw_source outputs when used as a reference
        self.add_parameter('ref_osc_output_freq',
                           label='Reference Oscillator Output Frequency',
                           get_cmd='SOUR:ROSC:OUTP:FREQ?',
                           set_cmd='SOUR:ROSC:OUTP:FREQ {}',
                           vals=vals.Enum('10MHz', '100MHz', '1000MHz'))
        # Frequency of the external reference mw_source uses
        self.add_parameter('ref_osc_external_freq',
                           label='Reference Oscillator External Frequency',
                           get_cmd='SOUR:ROSC:EXT:FREQ?',
                           set_cmd='SOUR:ROSC:EXT:FREQ {}',
                           vals=vals.Enum('10MHz', '100MHz', '1000MHz'))

        # IQ impairments
        self.add_parameter('IQ_impairments',
                           label='IQ Impairments',
                           get_cmd=':SOUR:IQ:IMP:STAT?',
                           set_cmd=':SOUR:IQ:IMP:STAT {}',
                           val_mapping=create_on_off_val_mapping(on_val='1',
                                                                 off_val='0'))
        self.add_parameter('I_offset',
                           label='I Offset',
                           get_cmd='SOUR:IQ:IMP:LEAK:I?',
                           set_cmd='SOUR:IQ:IMP:LEAK:I {:.2f}',
                           get_parser=float,
                           vals=vals.Numbers(-10, 10))
        self.add_parameter('Q_offset',
                           label='Q Offset',
                           get_cmd='SOUR:IQ:IMP:LEAK:Q?',
                           set_cmd='SOUR:IQ:IMP:LEAK:Q {:.2f}',
                           get_parser=float,
                           vals=vals.Numbers(-10, 10))
        self.add_parameter('IQ_gain_imbalance',
                           label='IQ Gain Imbalance',
                           get_cmd='SOUR:IQ:IMP:IQR?',
                           set_cmd='SOUR:IQ:IMP:IQR {:.2f}',
                           get_parser=float,
                           vals=vals.Numbers(-1, 1))
        self.add_parameter('IQ_angle',
                           label='IQ Angle Offset',
                           get_cmd='SOUR:IQ:IMP:QUAD?',
                           set_cmd='SOUR:IQ:IMP:QUAD {:.2f}',
                           get_parser=float,
                           vals=vals.Numbers(-8, 8))
        
        self.add_parameter('pulse_mode',
                           label='pulse_mode',
                           get_cmd='SOUR:PULM:MODE?',
                           set_cmd='SOUR:PULM:MODE{}',
                           get_parser=float,
                           ) #Sets the mode of the pulse generator. 
                             #SINGle (Enables single pulse generation) or DOUBle (Enables double pulse generation. The two pulses are generated in one pulse period.)
        
        self.add_parameter('pulse_pol',
                           label='pulse_polarity',
                           get_cmd='SOUR:PULM:POL?',
                           set_cmd='SOUR:PULM:POL{}',
                           get_parser=float,
                           ) #Sets the polarity of the pulse modulator signal. This command is effective only for an external modulation signal.  Parms: NORMal | INVerted
        
        self.add_parameter('pulse_sour',
                           label='pulse_source',
                           get_cmd='SOUR:PULM:SOUR?',
                           set_cmd='SOUR:PULM:SOUR{}',
                           get_parser=float,
                           ) #Selects the source for pulse modulation. Parms: INTernal | EXTernal

        
        self.add_parameter('pow_mod_source',
                           label='pow_mod_source',
                           get_cmd='SOURPULM:STAT?',
                           set_cmd='SOUR:PULM:STAT{}',
                           get_parser=float,
                           ) #Activates(1) and de-activate(0) the pulse modulation.Parameters: 0 | 1 | OFF | ON 
        
        
        self.add_parameter('pulse_width',
                           label='pulse_width',
                           get_cmd='SOUR::PULM:WIDT?',
                           set_cmd='SOUR::PULM:WIDT {:.2f}',
                           get_parser=float,
                           vals=vals.Numbers(20,100)) #20ns to 100 s, increment: 10 ns 
                                                        #Sets the width of the generated pulse. The width determines the pulse length.
                                                        #The pulse width must be at least 20ns less than the set pulse period
        
        
        
        
        self.add_function('reset', call_cmd='*RST')
        self.add_function('run_self_tests', call_cmd='*TST?')

        self.connect_message()





    def on(self) -> None:
        self.status('on')

    def off(self) -> None:
        self.status('off')


class RohdeSchwarz_SGS100A(RohdeSchwarzSGS100A):
    pass