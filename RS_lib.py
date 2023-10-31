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

        #trigger
        self.add_parameter('trigger_source',
                           label='trigger source',
                           get_cmd='SOUR:LIST:TRIG:SOUR?',
                           set_cmd='SOUR:LIST:TRIG:SOUR{}',
                           vals=vals.Enum('IMM','BUS','EXT')
        )

        self.add_parameter('trigger_mode',
                           label='trigger mode',
                           get_cmd='SOUR:LIST:TRIG:MODE?',
                           set_cmd='SOUR:LIST:TRIG:MODE{}',
                           vals=vals.Enum('AUTO','EXT','EGAT', 'SING', 'ESIN')
        )
        
           #Switches the local state of the continuous power measurement by R&S NRP power sensors on and off.
           #Switching off local state enhances the measurement performance during remote control.
        self.add_parameter('NRP_set_status',
                           label='NRP_set_status',
                           get_cmd='INIT:POW:CONT?',
                           set_cmd='INIT:POW:CONT{}',
                           vals=vals.Enum('0','1','ON','OFF') 
                         
                            )
        

        #SOURce:SWEep Subsystem. The SOURce:SWEep subsystem contains the commands for configuring RF sweep signals.

        #Provided for compatibility between SCPI and Rohde & Schwarz commands
        self.add_parameter('RS_compatibility',
                        label='RS_compatibility',
                        get_cmd='SWE:TYPE?',
                        set_cmd='SWE:TYPE{}',
                        vals=vals.Enum('ADV','STAN')  #  *RST: n.a. (factory preset: STANdard)
                        
                        )
        #Sets the dwell time for a level sweep step.
        self.add_parameter('dwell_time_step',
                        label='dwell_time_step',
                        get_cmd='SOUR:SWE:POW:DWEL?',
                        set_cmd='SOUR:SWE:POW:DWEL{}',
                        get_parser=float,
                        vals=vals.Numbers(3e-3,100)  #  Increment: 100E-6; *RST: 10E-3;Default unit: s
                        
                        )
        #Sets the dwell time for a level sweep step.
        self.add_parameter('dwell_time_step_pow',
                        label='dwell_time_step_pow',
                        get_cmd='SOUR:SWE:POW:DWEL?',
                        set_cmd='SOUR:SWE:POW:DWEL{}',
                        get_parser=float,
                        vals=vals.Numbers(0.001, 100)  #  Increment: 100E-6 ;*RST: 0.01
                        
                        )
        
         #Selects frequency sweep type.
        """
        STEPped | ANALog
        STEPped
        Performs a frequency sweep.
        ANALog
        Performs a continuous analog frequency sweep (ramp),
        synchronized with the sweep time [:SOURce<hw>]:SWEep[:
        FREQuency]:TIME.
        *RST: STEPped
        
        """

        self.add_parameter('freq_sweep_type',
                        label='freq_sweep_type',
                        get_cmd='SOUR:SWE:GEN?',
                        set_cmd='SOUR:SWE:GEN{}',
                        vals=vals.Enum('STEP','ANAL')  #Increment: 0.01 ;  *RST: 0
                        
                        )

        #Sets the cycle mode for the level sweep

        """
        AUTO
        Each trigger triggers exactly one complete sweep
        MANual
        The trigger system is not active. You can trigger every step individually
        with the command [:SOURce<hw>]:POWer:MANual.
        The level value increases at each step by the value that you
        define with [:SOURce<hw>]:POWer:STEP[:INCRement].
        Values directly entered with the command [:SOURce<hw>]:
        POWer:MANual are not taken into account.
        STEP
        Each trigger triggers one sweep step only. The level increases
        by the value entered with [:SOURce<hw>]:POWer:STEP[:
        INCRement].
        
        """
        self.add_parameter('cycle_mode',
                        label='cycle_mode',
                        get_cmd='SOUR:SWE:POW:MODE?',
                        set_cmd='SOUR:SWE:POW:MODE{}',
                        vals=vals.Enum('AUTO','MAN','STEP')  #  *RST: AUTO
                        
                        )

        #Queries the level sweep spacing. The sweep spacing for level sweeps is always linear
        self.add_parameter('query_lvlsweep_spacing',
                        label='query_lvlsweep_spacing',
                        get_cmd='SOUR:SWE:POW:SPAC:MODE?',
                        set_cmd='SOUR:SWE:POW:SPAC:MODE?{}',
                        vals=vals.Enum('LIN')  #  *RST: AUTO
                        
                        )
        
        #Sets a logarithmically determined step size for the RF level sweep. The level is 
        #increased by a logarithmically calculated fraction of the current level

        self.add_parameter('log_det_step_size',
                        label='log_det_step_size',
                        get_cmd='SOUR:SWE:POW:STEP:LOG?',
                        set_cmd='SOUR:SWE:POW:STEP:LOG?{}',
                        get_parser=float, #The unit dB is mandatory.
                        vals=vals.Numbers(0.01, 139)  # Increment: 0.01 , *RST: 1, Default unit: dB
                        
                        )


        #Sets the dwell time for a frequency sweep step.
        self.add_parameter('dwell_time_freqsweep_step',
                        label='dwell_time_freqsweep_step',
                        get_cmd='SOUR:SWE:FREQ:DWEL?',
                        set_cmd='SOUR:SWE:FREQ:DWEL{}',
                        get_parser=float, 
                        vals=vals.Numbers(0.001, 100)  # Increment: 100E-6 ; *RST: 0.01
                        
                        )

        #Sets the cycle mode for the frequency sweep
        """
        AUTO
        Each trigger event triggers exactly one complete sweep.
        MANual
        The trigger system is not active. You can trigger every step individually
        by input of the frequencies with the command [:
        SOURce<hw>]:FREQuency:MANual.
        STEP
        Each trigger event triggers one sweep step. The frequency
        increases by the value entered with [:SOURce<hw>]:SWEep[:
        FREQuency]:STEP[:LINear] (linear spacing) or [:
        SOURce<hw>]:SWEep[:FREQuency]:STEP:LOGarithmic
        (logarithmic spacing).
        
        """

        self.add_parameter('cycle_mode_freqsweep',
                        label='cycle_mode_freqsweep',
                        get_cmd='SOUR:SWE:FREQ:MODE?',
                        set_cmd='SOUR:SWE:FREQ:MODE{}',
                        vals=vals.Enum('AUTO','MAN','STEP')  # *RST: AUTO
                        
                        )

        #Sets the number of steps within the RF frequency sweep range.
        MAX_STEP= 4
        self.add_parameter('steps_number_RF_sweep',
                        label='steps_number_RF_sweep',
                        get_cmd='SOUR:SWE:FREQ:POIN?',
                        set_cmd='SOUR:SWE:FREQ:POIN{}',
                        get_parser = int,
                        vals=vals.Numbers(2,MAX_STEP)  # *RST: AUTO
                        
                        )

        #Selects the mode for the calculation of the frequency intervals, with which the current 
        #frequency at each step is increased or decreased.
        """
        LINear
        Sets a fixed frequency value as step width and adds it to the current
        frequency.
        The linear step width is entered in Hz, see [:SOURce<hw>]:
        SWEep[:FREQuency]:STEP[:LINear].
        LOGarithmic
        Sets a constant fraction of the current frequency as step width
        and adds it to the current frequency.
        The logarithmic step width is entered in %, see [:
        SOURce<hw>]:SWEep[:FREQuency]:STEP:LOGarithmic
        
        """
        self.add_parameter('calc_freq_int_mode',
                        label='calc_freq_int_mode',
                        get_cmd='SOUR:SWE:FREQ:SPAC?',
                        set_cmd='SOUR:SWE:FREQ:SPAC{}',
                        vals=vals.Enum('LIN','LOG')  # *RST: LIN
                        
                        )

        #[:SOURce<hw>]:SWEep:POWer:SHAPe <Shape>; [:SOURce<hw>]:SWEep[:FREQuency]:SHAPe <Shape>
        #Determines the waveform shape for a frequency sweep sequence.

        self.add_parameter('waveform_shape_freqsweep',
                        label='waveform_shape_freqsweep',
                        get_cmd='SOUR:SWE:POW:SHAP?',
                        set_cmd='SOUR:SWE:POW:SHAP{}',
                        vals=vals.Enum('SAWT','TRI')  # *RST: SAWTooth
                        
                        )
        
        #Executes an RF frequency sweep.
        self.add_parameter('freq_sweep_execute',
                        label='freq_sweep_execute',
                        get_cmd='SOUR:SWE:POW:EXEC?',
                        set_cmd='SOUR:SWE:POW:EXEC{}',
                        vals=vals.Enum()  
                        
                        )
        
        #Activates that the signal changes to the start frequency value while it is waiting for the next trigger event. 
        # You can enable this feature, when you are working with sawtooth shapes in sweep mode "Single" or "External Single".
        self.add_parameter('signal_changes_active',
                        label='signal_changes_active',
                        get_cmd='SOUR:SWE:POW:RETR?',
                        set_cmd='SOUR:SWE:POW:RETR{}',
                        vals=vals.Enum('ON','OFF','1','0') #*RST:0   
                        
                        )
        #Queries the current sweep state
        self.add_parameter('query_sweep_state',
                        label='query_sweep_state',
                        get_cmd='SOUR:SWE:POW:RUNN?',
                        set_cmd='SOUR:SWE:POW:RUNN?{}',
                        vals=vals.Enum('ON','OFF','1','0')  
                        
                        )
        
        #Sets a logarithmically determined step width for the RF frequency sweep. The value is 
        # added at each sweep step to the current frequency.
        self.add_parameter('log_det_step_width',
                    label='log_det_step_width',
                    get_cmd='SOUR:SWE:FREQ:STEP:LOG?',
                    set_cmd='SOUR:SWE:FREQ:STEP:LOG?{}',
                    get_parser=float,
                    vals=vals.Numbers(0.01,100)  #Increment: 1E-3 ; *RST: 1 ; Default unit: PCT
                    
                    )
        #Sets the step width for linear sweeps.
        dt = (STOP - STARt)
        self.add_parameter('lin_det_step_width',
                    label='lin_det_step_width',
                    get_cmd='SOUR:SWE:FREQ:STEP:LIN?',
                    set_cmd='SOUR:SWE:FREQ:STEP:LIN?{}',
                    get_parser=float, #Hz
                    vals=vals.Numbers(0.001 , dt )  #Increment: 0.01
                    
                    )
        
        #Resets all active sweeps to the starting point
        self.add_function('reset_all_sweep', call_cmd='SOUR:SWE:RES:ALL')

        #Sets the duration of a frequency ramp sweep step.
        self.add_parameter('ramp_sweep_duration',
                    label='ramp_sweep_duration',
                    get_cmd='SOUR:SWE:FREQ:TIME?',
                    set_cmd='SOUR:SWE:FREQ:TIME{}',
                    get_parser=float, #s
                    vals=vals.Numbers(0.01 , 100)  #Increment: 1E-4; *RST: 0.015
                    
                    )


        # level offset at the sensor input in dB. Must be activate with the next parameter:sensor offset state
        self.add_parameter('lvl_offset',
                        label='lvl_offset',
                        get_cmd='SENS{channum}:POW:SWE:FREQ:SENS:OFFS:STAT?',
                        set_cmd='SENS{channum}:POW:SWE:FREQ:SENS:OFFS:STAT{}',
                        vals=vals.Numbers(-100,100)  #Increment: 0.01 ;  *RST: 0
                        
                        )
        
       



        # Activates the specified level offset.
        self.add_parameter('offset_state',
                        label='offset_state',
                        get_cmd='SENS{channum}:POW:SWE:FREQ:SENS:OFFS:STAT?',
                        set_cmd='SENS{channum}:POW:SWE:FREQ:SENS:OFFS:STAT{}',
                        vals=vals.Enum('ON','OFF','1','0')
                        
                        )
        # Sets the start frequency for the frequency power analysis with separate frequencies.(frequency versus
        # power measurement.) 
        self.add_parameter('start_freq',
                        label='start_freq',
                        get_cmd='SENSe{channum}:POW:SWE:FREQ:SENS:SRAN:STAR?',
                        set_cmd='SENSe{channum}:POW:SWE:FREQ:SENS:SRAN:STAR{}',
                        vals=vals.Numbers(0,1e12) # *RST: 1E6
                        
                        )
        # Sets the stop frequency for the frequency power analysis with separate frequencies(frequency versus
        # power measurement.)
        self.add_parameter('stop_freq',
                        label='stop_freq',
                        get_cmd='SENSe{channum}:POW:SWE:FREQ:SENS:SRAN:STOP?',
                        set_cmd='SENSe{channum}:POW:SWE:FREQ:SENS:SRAN:STOP{}',
                        vals=vals.Numbers(0,1e12) # *RST: 1E6
                        
                        )            

        """
        Example: SENS:SWE:FREQ:SENS2:SRAN:STAT ON
        Activates use of a separate frequency range for frequency versus
        power measurement.
        SENS:SWE:FREQ:SENS2:STAR 2.0GHZ
        Sets a sweep start at 2 GHz irrespective of the current signal
        generator frequency settings.
        SENS:SWE:FREQ:SENS2:STOP 2.9GHZ
        Sets a sweep stop at 2.9 GHz irrespective of the current signal
        generator frequency settings.

        """

        #Activates the use of a frequency range for the power measurement that is different to 
        # the set signal generator frequency range

        self.add_parameter('pow_meas_state',
                        label='power measurement (de)activation',
                        get_cmd='SENS{channum}:POW:SWE:FREQ:SENS:SRAN:STAT?',
                        set_cmd='SENS{channum}:POW:SWE:FREQ:SENS:SRAN:STAT{}',
                        vals=vals.Enum('ON','OFF','1','0') # *RST: 0
                        
                        ) 
        # Define the level offset the sensor input in dB
        self.add_parameter('set_offset_level',
                    label='set_offset_level',
                    get_cmd='SENS{channum}:POW:SWE:POW:SENS:OFFS?',
                    set_cmd='SENS{channum}:POW:SWE:POW:SENS:OFFS{}',
                    get_parser=float,
                    vals=vals.Numbers(-100,100) # Increment: 0.01, *RST: 0
        )

        # Activate a level offset at the sensor input
        self.add_parameter('offset_level_state',
                    label='offset_level_state',
                    get_cmd='SENS{channum}:POW:SWE:POW:SENS:OFFS:STAT?',
                    set_cmd='SENS{channum}:POW:SWE:POW:SENS:OFFS:STAT{}',
                    vals=vals.Enum('0','1','OFF','ON') 
        )

        # Defines the separate frequency used for power vs. power measurement.

        self.add_parameter('sep_freq_set',
                    label='sep_freq_set',
                    get_cmd='SENS{channum}:POW:SWE:POW:SENS:SFR?',
                    set_cmd='SENS{channum}:POW:SWE:POW:SENS:SFR{}',
                    vals=vals.Numbers(0,1e12)   # Increment: 1; *RST: 1E6
                     
        )
        # Activates the use of a separate frequency than the generator frequency for power analysis

        self.add_parameter('sep_freq_activate',
                    label='sep_freq_activate',
                    get_cmd='SENSe{channum}:POW:SWE:POW:SENS:SFR:STAT?',
                    set_cmd='SENSe{channum}:POW:SWE:POW:SENS:SFR:STAT{}',
                    vals=vals.Enum('0','1','OFF','ON')   # *RST: 0
                     
        )


        # Defines the level offset at the sensor input in dB
        self.add_parameter('sep_freq_time_set',
                    label='sep_freq_time_set',
                    get_cmd='SENSe{channum}:POW:SWE:TIME:SENS:OFFS?',
                    set_cmd='SENSe{channum}:POW:SWE:TIME:SENS:OFFS{}',
                    get_parser=float,
                    vals=vals.Numbers(-100,100)   # Increment: 0.01 ; *RST: 0
                            )
        #Activates a level offset at the sensor input.

        self.add_parameter('sep_freq_time_activate',
                    label='sep_freq_time_activate',
                    get_cmd='SENS{channum}:POW:SWE:TIME:SENS:OFFS:STAT?',
                    set_cmd='SENS{channum}:POW:SWE:TIME:SENS:OFFS:STAT{}',
                    vals=vals.Enum('0','1','OFF','ON')   # *RST: 0
                             )


        #Enables pulse data analysis. The measurement is started with command INITiate.
        #The command is only available in time measurement mode and with R&S NRPZ81 power sensors.
        self.add_parameter('pulse_data_an_state',
                    label='pulse_data_an_state',
                    get_cmd='SENS{channum}POW:SWE:TIME:SENS:PULS:STAT?',
                    set_cmd='SENS{channum}POW:SWE:TIME:SENS:PULS:STAT?{}',
                    vals=vals.Enum('0','1','OFF','ON')   # *RST: 0
        )
        # how the threshold parameters for pulse analysis are calculated.
        # Activates threshold calculation related to volt/power. only available in time measurement mode and with R&S 
        # NRPZ81 power sensors.

        self.add_parameter('sense_time_treshold_base',
                    label='sense_time_treshold_base',
                    get_cmd='SENSe{channum}:POW:SWE:TIME:SENS:PULS:THR:BASE?',
                    set_cmd='SENSe{channum}:POW:SWE:TIME:SENS:PULS:THR:BASE{}',
                    vals=vals.Enum('VOLT','POW')   # *RST: VOLT
        )

        #Sets the upper reference level in terms of percentage of the overall pulse level (power 
        # or voltage). The distal power defines the end of the rising edge and the start of the falling
        # edge of the pulse. ONLY AVAILABLE in time measurement mode and with R&S NRPZ81 power sensors
         
        self.add_parameter('upper_ref_lvl',
                    label='upper refrence level',
                    get_cmd='SENS{channum}:POW]:SWE:TIME:SENS:PULS:THR:POW:HREF?',
                    set_cmd='SENS{channum}:POW]:SWE:TIME:SENS:PULS:THR:POW:HREF{}',
                    get_parser=float,
                    vals=vals.Numbers(0., 100.)   # Increment: 0.01 ; *RST: 90
        )

        #Sets the lower reference level in terms of percentage of the overall pulse level. The
        # proximal power defines the start of the rising edge and the end of the falling edge of
        # the pulse. ONLY AVAILABLE in time measurement mode and with R&S NRPZ81 power sensors

        
        self.add_parameter('lower_ref_lvl',
                    label='lower refrence level',
                    get_cmd='SENSe{channum}:POW:SWE:TIME:SENS:PULS:THR:POW:LREF?',
                    set_cmd='SENSe{channum}:POW:SWE:TIME:SENS:PULS:THR:POW:LREF{}',
                    get_parser=float,
                    vals=vals.Numbers(0.0, 100.0)   # Increment: 0.01 ; *RST: 10
        )


        #Sets the medial reference level in terms of percentage of the overall pulse level (power 
        # or voltage related). This level is used to define pulse width and pulse period.
        #ONLY AVAILABLE in time measurement mode and with R&S NRPZ81 power sensors

        self.add_parameter('mid_ref_lvl',
                    label='mid refrence level',
                    get_cmd='SENS{channum}:POW:SWE:TIME:SENS:PULS:THR:POW:REF?',
                    set_cmd='SENS{channum}:POW:SWE:TIME:SENS:PULS:THR:POW:REF{}',
                    get_parser=float,
                    vals=vals.Numbers(0.0, 100.0)   # Increment: 0.01 ; *RST: 50
        )

        #Defines the separate frequency used for power vs. time measurement.

        self.add_parameter('define_sep_fr',
                    label='define_separate_frequency',
                    get_cmd='SENS{channum}[:POW]:SWE:TIME[:SENS]:SFR?',
                    set_cmd='SENS{channum}[:POW]:SWE:TIME[:SENS]:SFR{}',
                    get_parser=float,
                    vals=vals.Numbers(0.,1.e12)   # Increment: 1 ; *RST: 1e6
        )

        #Activates the use of a different frequency for the power measurement.

        self.add_parameter('sweep_time_state',
                    label='sweep_time_state',
                    get_cmd='SENS{channum}}:POW:SWE:TIME:SENS:SFR:STAT?',
                    set_cmd='SENS{channum}}:POW:SWE:TIME:SENS:SFR:STAT{}',
                    vals=vals.Enum('ON','OFF','1','0')   #*RST: 0
        )

        # Sets the trigger level, the hysteresis and the dropout time to default values

        self.add_parameter('set_thd_default',
                    label='set_thd_default',
                    get_cmd='SENS{channum}:POW:SWE:TIME:SENS:TRIG:AUTO?',
                    set_cmd='SENS{channum}:POW:SWE:TIME:SENS:TRIG:AUTO{}',
                    vals=vals.Enum('ONCE')
        )


        #Determines the minimum time for which the signal must be below (above) the power level defined by level and hysteresis before triggering can occur again.

        self.add_parameter('set_dropout_time',
                    label='set_dropout_time',
                    get_cmd='SENS{channu}:POW:SWE:TIME:SENS:TRIG:DTIM?',
                    set_cmd='SENS{channu}:POW:SWE:TIME:SENS:TRIG:DTIM?{}',
                    get_parser=float,
                    vals=vals.Numbers(0.,10.)  #*RST 200E-9  
        )

        


        # Sets the hysteresis of the internal trigger threshold. Hysteresis is the magnitude (in dB) the trigger signal level must drop below the trigger threshold (positive trigger slope) 
        # before triggering can occur again.
        
        self.add_parameter('set_hyst_int_trigger',
                    label='set_hyst_int_trigger',
                    get_cmd='SENS{channum}:POW:SWE:TIME:SENS:TRIG:HYST?',
                    set_cmd='SENS{channum}:POW:SWE:TIME:SENS:TRIG:HYST{}',
                    get_parser=float,
                    vals=vals.Numbers(0.,10.)  # Increment: 0.001 ; *RST: 0.5  
        )
        

        #Sets the trigger threshold.

        self.add_parameter('trigger_level',
                    label='trigger_level',
                    get_cmd='SENS{channum}:POW:SWE:TIME:SENS:TRIG:LEV?',
                    set_cmd='SENS{channum}:POW:SWE:TIME:SENS:TRIG:LEV{}',
                    get_parser=float,
                    vals=vals.Numbers(-200.,100.)  # Increment: 0.001 ; *RST: 1
        )


        #Sets the polarity of the active slope for the trigger signals 

        self.add_parameter('trigger_pol',
            label='trigger_pol',
            get_cmd='SENS{channum}:POW:SWE:TIME:SENS:TRIG:SLOP?',
            set_cmd='SENS{channum}:POW:SWE:TIME:SENS:TRIG:SLOP{}',
            get_parser=float,
            vals=vals.Numbers(-200.,100.)  # Increment: 0.001 ; *RST: 1
        )


        #Selects if the measurement is free running (FREE) or starts only after a trigger event. The trigger can be applied internally or externally.
       
        self.add_parameter('trg_sens',
            label='trg_sens',
            get_cmd='SENSe{channum}:POW:SWE:TIME:SENS:TRIG:SOUR?',
            set_cmd='SENSe{channum}:POW:SWE:TIME:SENS:TRIG:SOUR{}',
            vals=vals.Enum("FREE","AUTO","INT","EXT") 
        )


        #The command activates the autozero function. The RF power source must be switched off or disconnected from the sensor
        # before starting the autozero function.

        self.add_parameter('autozero',
            label='autozero',
            get_cmd='SENS{channum}:POW:ZERO?',
            set_cmd='SENS{channum}:POW:ZERO{}',
            vals=vals.Enum() 
        )

        #Aborts the power analysis with NRP power sensors.

        self.add_parameter('sweep_abort',
            label='sweep_abort',
            get_cmd='SENS:POW:SWE:ABOR?',
            set_cmd='SENS:POW:SWE:ABOR{}',
            vals=vals.Enum() 
        )

        #Generates a reference curve for "Frequency" measurement.

        self.add_parameter('ref_curv',
            label='ref_curv',
            get_cmd='SENS:POW:SWE:FREQ:REF:DATA:COPY?',
            set_cmd='SENS:POW:SWE:FREQ:REF:DATA:COPY{}',
            vals=vals.Enum() 
        )

        #Queries the number of points from the reference curve in "Frequency" measurement. Query only

        self.add_parameter('n_points_from_reference',
            label='n_points_from_reference',
            get_cmd='SENS:POW:SWE:FREQ:REF:DATA:POIN?',
            set_cmd='SENS:POW:SWE:FREQ:REF:DATA:POIN{}',
            get_parser=int,
            vals=vals.Numbers(10,1000) 
        )


        #Sets or queries the x values of the two reference points, i.e. "Frequency X (Point A)" 
        # and "Frequency X (Point B)" in "Frequency" measurement.


        self.add_parameter('x_set_freq_meas',
        label='x_set_freq_meas',
        get_cmd='SENS:POW:SWE:FREQ:REF:DATA:XVAL?',
        set_cmd='SENS:POW:SWE:FREQ:REF:DATA:XVAL{}',
        get_parser=str,
        vals=vals.Enum() 
        )



        #Sets or queries the y values of the two reference points, i.e."Pow Y (Point A)" and 
        # "Power Y (Point B)" in "Frequency" measurement.

        self.add_parameter('y_set_freq_meas',
        label='y_set_freq_meas',
        get_cmd='SENS:POW:SWE:FREQ:REF:DATA:YVAL?',
        set_cmd='SENS:POW:SWE:FREQ:REF:DATA:YVAL{}',
        get_parser=str,
        vals=vals.Enum() 
        )


        #Selects single or continuous mode for measurement mode frequency in power analysis.

        self.add_parameter('freq_mode_poweran_set',
        label='freq_mode_poweran_set',
        get_cmd='SENS:POW:SWE:FREQ:RMOD?',
        set_cmd='SENS:POW:SWE:FREQ:RMOD{}',
        vals=vals.Enum("CONT","SING")   #*RST: CONT
        )


        #Selects the spacing for the frequency power analysis.

        self.add_parameter('spacing_freqan_set',
        label='spacing_freqan_set',
        get_cmd='SENS:POW:SWE:FREQ:SPAC:MODE?',
        set_cmd='SENS:POW:SWE:FREQ:SPAC:MODE{}',
        vals=vals.Enum("LIN","LOG")  
        )



        #Sets the start frequency for the frequency mode

        self.add_parameter('start_freq',
        label='start_freq',
        get_cmd='SENS:POW:SWE:FREQ:STAR?',
        set_cmd='SENS:POW:SWE:FREQ:STAR{}',
        get_parser=float,
        vals=vals.Numbers(0, 1e12)  #*RST: 1E6
        )


        #Sets the number of measurement steps for the frequency mode.

        self.add_parameter('steps_num_freqmode',
        label='steps_num_freqmode',
        get_cmd='SENS:POW:SWE:FREQ:STEP?',
        set_cmd='SENS:POW:SWE:FREQ:STEP{}',
        get_parser=int,
        vals=vals.Numbers(1, 1000 )  #*RST: 200
        )


        #Sets the stop frequency for the frequency mode.
        self.add_parameter('stop_freq',
        label='stop_freq',
        get_cmd='SENS:POW:SWE:FREQ:STOP?',
        set_cmd='SENS:POW:SWE:FREQ:STOP{}',
        get_parser=float,
        vals=vals.Numbers(0, 1e12)  #*RST: 22GHZ
        )

        #Selects the mode in terms of speed and precision of the response of a measurement
        """
        FAST
        Selection FAST leads to a fast measurement with a short integration
        time for each measurement step.
        NORMal
        NORMal leads to a longer but more precise measurement due
        to a higher integration time for each step.
        """
        self.add_parameter('speed_mode_meas',
        label='speed_mode_meas',
        get_cmd='SENS:POW:SWE:FREQ:TIM:MODE?',
        set_cmd='SENS:POW:SWE:FREQ:TIM:MODE{}',
        vals=vals.Enum("FAST","NORM","HPR")  #*RST: FAST
        )

        #Activates autoscaling of the Y axis of the diagram.
        """
        OFF
        Auto scaling is deactivated. If switching from activated to deactivated
        Auto scaling, the scaling is maintained.
        CEXPanding | FEXPanding
        Auto scale is activated. The scaling of the Y-axis is selected in
        such a way, that the trace is always visible. To this end, the
        range is expanded if the minimum or maximum values of the
        trace move outside the current scale. The step width is 5 dB for
        selection course and variable in the range of 0.2 db to 5 dB for
        selection fine.
        CFLoating | FFLoating
        Auto scale is activated. The scaling of the Y-axis is selected in
        such a way, that the trace is always visible. To this end, the
        range is either expanded if the minimum or maximum values of
        the trace move outside the current scale or scaled down if the
        trace fits into a reduced scale. The step width is 5 dB for selection
        course and variable in the range of 0.2 db to 5 dB for selection
        fine.
        """

        self.add_parameter('y_autoscale',
        label='y_autoscale',
        get_cmd='SENS:POW:SWE:FREQ:YSC:AUTO?',
        set_cmd='SENS:POW:SWE:FREQ:YSC:AUTO{}',
        vals=vals.Enum("OFF","CEXP","FEXP","CFL","FFL")  #*RST: CEXPanding
        )



        #Resets the Y scale to suitable values after the use of auto scaling in the expanding mode.

        self.add_parameter('y_scale_rst',
        label='y_scale_rst',
        get_cmd='SENS:POW:SWE:FREQ:YSC:AUTO:RES?',
        set_cmd='SENS:POW:SWE:FREQ:YSC:AUTO:RES{}',
        vals=vals.Enum()
        )


        #Sets the maximum value for the y axis of the measurement diagram  (dBm)

        self.add_parameter('max_y_axis',
        label='max_y_axis',
        get_cmd='SENS:POW:SWE:FREQ:YSC:MAX?',
        set_cmd='SENS:POW:SWE:FREQ:YSC:MAX{}',
        get_parser=float,
        vals=vals.Numbers(-200,100) # increment: 0.01 ; *RST: 40
        )

        #Sets the minimum value for the y axis of the measurement diagram.

        self.add_parameter('min_y_axis',
        label='min_y_axis',
        get_cmd='SENS:POW:SWE:FREQ:YSC:MIN?',
        set_cmd='SENS:POW:SWE:FREQ:YSC:MIN{}',
        get_parser=float,
        vals=vals.Numbers(-200,100) # increment: 0.01 ; *RST: -40
        )



    #Queries the measurement data directly. The data is transferred to the remote client as data stream.
    #Readable ASCII data is available for hardcopy language CSV. The representation of 
    #the values depends on the selected orientation for the CSV format.

        """
        SENS:SWE:HCOP:DEV:LANG CSV
        selects output format *.csv.
        SENS:SWE:HCOP:DEV:LANG:CSV:ORI HOR
        selects horizontal orientation
        SENS:SWE:HCOP:DEV:LANG:CSV:SEP SEM
        selects ";" as the separator between the values
        SENS:SWE:HCOP:DEV:LANG:CSV:DPO DOT
        selects "." as decimal point
        SENS:SWE:HCOP:DATA?
        queries the measurement data of the current traces
        Response:
        #2651009500000;1019000000;1028500000;1038000000
        -9.5;-9.7;-6.3;-2.5
        The hash symbol # introduces the data block. The next number
        indicates how many of the following digits describe the length of
        the data block. In the example, the 2 following digit indicates the
        length to be 65 characters.
        Because horizontal representation is selected, a row with all the
        x-values of the active trace (frequency) follows. The second row
        contains all the y-values of the active trace (power). The rows
        end with a new line (each counts as one character).
        Note: if more than one trace is active, the third row contains the
        x values of the second active trace, and so on.        
                
        
        """


        #Defines the output device. The setting is fixed to FILE, i.e. the hardcopy is stored in a file.

        self.add_parameter('output_dev',
        label='output_dev',
        get_cmd='SENS:POW:SWE:HCOP:DEV?',
        set_cmd='SENS:POW:SWE:HCOP:DEV{}',
        vals=vals.Enum("FILE" , "PRIN") # *RST: FILE
        )


        #Selects the bitmap graphic format for the screenshot of the power analysis trace.

        self.add_parameter('bitmap_format',
        label='bitmap_format',
        get_cmd='SENS:POW:SWE:HCOP:DEV:LANG?',
        set_cmd='SENS:POW:SWE:HCOP:DEV:LANG{}',
        vals=vals.Enum("BMP","JPG","XPM","PNG","CSV") # *RST: BMP
        )
    

        #Defines which character is used as the decimal point of the values, either dot or comma.

        self.add_parameter('decimal_point',
        label='decimal_point',
        get_cmd='SENS:POW:SWE:HCOP:DEV:LANG:CSV:DPO?',
        set_cmd='SENS:POW:SWE:HCOP:DEV:LANG:CSV:DPO{}',
        vals=vals.Enum("DOT","COMM") # *RST: DOT
        )


        # Defines whether each row (or column depending on the orientation) should be preceded 
        # by a header containing information about the trace

        self.add_parameter('header_csv_row',
        label='header_csv_row',
        get_cmd='SENS:POW:SWE:HCOP:DEV:LANG:CSV:HEAD?',
        set_cmd='SENS:POW:SWE:HCOP:DEV:LANG:CSV:HEAD{}',
        vals=vals.Enum("OFF","STAN") # *RST: OFF
        )
        
        #Defines the orientation of the X/Y value pairs.

        self.add_parameter('csv_orientation',
        label='csv_orientation',
        get_cmd='SENS:POW:SWE:HCOP:DEV:LANG:CSV:ORI?',
        set_cmd='SENS:POW:SWE:HCOP:DEV:LANG:CSV:ORI{}',
        vals=vals.Enum("HOR","VERT") # *RST: VERT
        )

        #Defines which character is to separate the values, either tabulator, semicolon, comma or blank.
        
        self.add_parameter('csv_separator',
        label='csv_separator',
        get_cmd='SENS:POW:SWE:HCOP:DEV:LANG:CSV:COL:SEP?',
        set_cmd='SENS:POW:SWE:HCOP:DEV:LANG:CSV:COL:SEP{}',
        vals=vals.Enum("TAB","SEM","COMM","BLAN") # *RST: COMM
        )

        #Sets the size of the hardcopy in number of pixels. The first value of the size setting 
        # defines the width, the second value the height of the image.

        self.add_parameter('hcopy_size',
        label='hcopy_size',
        get_cmd='SENS:POW:SWE:HCOP:DEV:SIZE?',
        set_cmd='SENS:POW:SWE:HCOP:DEV:SIZE{}',
        vals=vals.Enum("320,240","640,480 ","800,600" ,"1024,768") # *RST: 320,240
        )


        #Creates of selects a file for storing the hardcopy after the :SENSe[:POWer]:SWEep:HCOPy[:EXECute]
        #directory is either defined with the command MMEMory:CDIR or the path is specified together with the file name 


        self.add_parameter('hcopy_size',
        label='hcopy_size',
        get_cmd='SENS:POW:SWE:HCOP:FILE:NAME?',
        set_cmd='SENS:POW:SWE:HCOP:FILE:NAME{}',
        get_parser = str,
        vals=vals.Enum("") 
        )


        #Activates/deactivates automatic naming of the hardcopy files.

        self.add_parameter('autonaming_state',
        label='autonaming_state',
        get_cmd='SENS:SWE:HCOP:FILE:AUTO:STAT?',
        set_cmd='SENS:SWE:HCOP:FILE:AUTO:STAT{}',
        vals=vals.Enum("ON","OFF","1","0")  # *RST 1
        )


        #Defines the directory into which the hardcopy files are stored if auto naming is activated

        self.add_parameter('hcopy_dir',
        label='hcopy_dir',
        get_cmd='SENS:POW:SWE:HCOP:FILE:NAME:AUTO:DIR?',
        set_cmd='SENS:POW:SWE:HCOP:FILE:NAME:AUTO:DIR{}',
        get_parser = str,
        vals=vals.Enum("") 
        )

        #Deletes all files with extensions bmp , img, png, xpm and csv in the directory set for automatic naming.

        self.add_parameter('delete_all_*_files',
        label='delete_all_*_files',
        get_cmd='SENS:POW:SWE:HCOP:FILE:NAME:AUTO:DIR:CLE?',
        set_cmd='SENS:POW:SWE:HCOP:FILE:NAME:AUTO:DIR:CLE{}',
        vals=vals.Enum("") 
        )


        #Queries the file name generated with the automatic naming settings
        """
        Note: As default the automatically generated file name is composed of: 
        >PAth>/<Prefix><YYYY><MM><DD><Number>.<Format>. 
        Each component can be deactivated/activated separately to individually design the file name.
        """

        self.add_parameter('query_all_*_files',
        label='query_all_*_files',
        get_cmd='SENS:POW:SWE:HCOPy:FILE[:NAME]:AUTO:FILE?',
        set_cmd='SENS:POW:SWE:HCOPy:FILE[:NAME]:AUTO:FILE{}',
        get_parser = str,
        vals=vals.Enum("") 
        )

        #Queries the day of the date part in the automatic file name.
        self.add_parameter('query_day',
        label='query_day',
        get_cmd='SENS:POW:SWE:HCOP:FILE:NAME:AUTO:FILE:DAY?',
        set_cmd='SENS:POW:SWE:HCOP:FILE:NAME:AUTO:FILE:DAY{}',
        get_parser = int,
        vals=vals.Numbers(1, 31)  #*RST: 1
        )

        #Activates the usage of the day in the automatic file name.

        self.add_parameter('day_in_filename_state',
        label='day_in_filename_state',
        get_cmd='SENS:POW:SWE:HCOP:FILE:NAME:AUTO:FILE:DAY:STAT?',
        set_cmd='SENS:POW:SWE:HCOP:FILE:NAME:AUTO:FILE:DAY:STAT{}',
        vals=vals.Enum("ON","OFF","1","0") #*RST: 1
        )

        #Queries the month of the date part in the automatic file name.

        self.add_parameter('query_month',
        label='query_month',
        get_cmd='SENS:POW:SWE:HCOP:FILE:NAME:AUTO:FILE:MONT?',
        set_cmd='SENS:POW:SWE:HCOP:FILE:NAME:AUTO:FILE:MONT{}',
        get_parser = int,
        vals=vals.Numbers(1,12)  #*RST: 1
        )


        #Activates the usage of the month in the automatic file name.

        self.add_parameter('month_in_filename_state',
        label='month_in_filename_state',
        get_cmd='SENS:POW:SWE:HCOP:FILE:NAME:AUTO:FILE:MONT:STAT?',
        set_cmd='SENS:POW:SWE:HCOP:FILE:NAME:AUTO:FILE:MONT:STAT{}',
        vals=vals.Enum("ON","OFF","1","0") #*RST: 1
        )


        #Queries the generated number in the automatic file name.

        self.add_parameter('query_number',
        label='query_number',
        get_cmd='SENS:POW:SWE:HCOP:FILE:NAME:AUTO:FILE:NUMB?',
        set_cmd='SENS:POW:SWE:HCOP:FILE:NAME:AUTO:FILE:NUMB{}',
        get_parser = int,
        vals=vals.Numbers(0,999999) #*RST: 0
        )



        #Sets the prefix part in the automatic file name.
        self.add_parameter('prefix_filename_set',
        label='prefix_filename_set',
        get_cmd='SENS:POW:SWE:HCOP:FILE:NAME:AUTO:FILE:PREF?',
        set_cmd='SENS:POW:SWE:HCOP:FILE:NAME:AUTO:FILE:PREF{}',
        get_parser = str,
        vals=vals.Enum("") 
        )



        #Activates the usage of the prefix in the automatic file name.

        self.add_parameter('prefix_in_filename_state',
        label='prefix_in_filename_state',
        get_cmd='SENS:POW:SWE:HCOP:FILE:NAME:AUTO:FILE:PREF:STAT?',
        set_cmd='SENS:POW:SWE:HCOP:FILE:NAME:AUTO:FILE:PREF:STAT{}',
        vals=vals.Enum("ON","OFF","1","0") #*RST: 1
        )

        #Queries the year of the date part in the automatic file name.
        self.add_parameter('query_year',
        label='query_year',
        get_cmd=':SENS:POW:SWE:HCOP:FILE:NAME:AUTO:FILE:YEAR?',
        set_cmd=':SENS:POW:SWE:HCOP:FILE:NAME:AUTO:FILE:YEAR?{}',
        get_parser = int,
        vals=vals.Numbers(1784,8000)  #*RST: 0
        )

        #Activates the usage of the year in the automatic file name.

        self.add_parameter('year_in_filename_state',
        label='year_in_filename_state',
        get_cmd='SENS:POW:SWE:HCOP:FILE:NAME:AUTO:FILE:YEAR:STAT?',
        set_cmd='SENS:POW:SWE:HCOP:FILE:NAME:AUTO:FILE:YEAR:STAT{}',
        vals=vals.Enum("ON","OFF","1","0") #*RST: 1
        )


        #Triggers the generation of a hardcopy of the current measurement diagram. The data 
        # is written into the file selected/created with the :SENSe[:POWer]:SWEep:HCOPy: FILE[:NAME]

        self.add_parameter('trg_hcopy',
        label='trg_hcopy',
        get_cmd='SENS:POW:SWE:HCOP:EXEC?',
        set_cmd='SENS:POW:SWE:HCOP:EXEC{}',
        vals=vals.Enum("") 
        )

#-------power analysis

        #Starts the power analysis with NRP power sensor.
        self.add_parameter('NRP_start',
        label='NRP_start',
        get_cmd='SENS:POW:SWE:INIT?',
        set_cmd='SENS:POW:SWE:INIT{}',
        vals=vals.Enum("") 
        )

        #Selects power versus frequency measurement (frequency response), power vs power 
        # measurement (power sweep, AM/AM) or power vs. time measurement.

        self.add_parameter('measurement_mode',
        label='measurement_mode',
        get_cmd='SENS:POW:SWE:MODE?',
        set_cmd='SENS:POW:SWE:MODE{}',
        vals=vals.Enum("FREQ" ,"POW","TIME") # *RST :FREQ
        )


        #Generates a reference curve for "Power" measurement.

        self.add_parameter('ref_curve_pow_meas',
        label='ref_curve_pow_meas',
        get_cmd='SENS:POW:SWE:POW:REF:DATA:COPY?',
        set_cmd='SENS:POW:SWE:POW:REF:DATA:COPY{}',
        vals=vals.Enum("")
        )


        #Queries the number of points from the reference curve in "Power" measurement.

        self.add_parameter('ref_curve_pow_meas',
        label='ref_curve_pow_meas',
        get_cmd='SENS:POW:SWE:POW:REF:DATA:POIN?',
        set_cmd='SENS:POW:SWE:POW:REF:DATA:POIN?{}',
        get_parser=int,
        vals=vals.Numbers(10, 1000)
        )

        #Sets or queries the x values of the two reference points, i.e. "Power X (Point A)" and "Power X (Point B)" 
        #in "Power" measurement. 
        self.add_parameter('x_set_pow_meas',
        label='x_set_pow_meas',
        get_cmd='SENS:POW:SWE:POW:REF:DATA:XVAL?',
        set_cmd='SENS:POW:SWE:POW:REF:DATA:XVAL{}',
        get_parser=str,
        vals=vals.Enum("")
        )
    
        #Sets or queries the y values of the two reference points, i.e. "Power Y (Point A)" and "Power Y (Point B)" 
        # in "Power" measurement

        self.add_parameter('y_set_pow_meas',
        label='y_set_pow_meas',
        get_cmd='SENS:POW:SWE:POW:REF:DATA:YVAL?',
        set_cmd='SENS:POW:SWE:POW:REF:DATA:YVAL{}',
        get_parser=str,
        vals=vals.Enum("")
        )

        #Selects single or continuous mode for measurement mode power in power analysis. freq_mode_poweran_set

        self.add_parameter('pow_mode_poweran_set',
        label='pow_mode_poweran_set',
        get_cmd='SENS:POW:SWE:POW:RMOD?',
        set_cmd='SENS:POW:SWE:POW:RMOD{}',
        vals=vals.Enum("SING", "CONT")  #*RST: CONT 
        )

        #Selects the spacing for the frequency power analysis. spacing_freqan_set

        self.add_parameter('spacing_poweran_set',
        label='spacing_poweran_set',
        get_cmd='SENS:POW:SWE:POW:SPAC:MODE?',
        set_cmd='SENS:POW:SWE:POW:SPAC:MODE{}',
        vals=vals.Enum("LIN")  #*RST: LIN 
        )

        #Sets the start level for the power versus power measurement
        self.add_parameter('start_power_analysis',
        label='start_power_analysis',
        get_cmd='SENS:POW:SWE:POW:STAR?',
        set_cmd='SENS:POW:SWE:POW:STAR{}',
        get_parser= float,
        vals=vals.Numbers(-145, 20)  # Increment: 0.01 ; *RST: 1MHZ
        )


        #Sets the number of measurement steps for the power versus power measurement.

        self.add_parameter('steps_num_powmode',
        label='steps_num_powmode',
        get_cmd='SENS:POW:SWE:POW:STEP?',
        set_cmd='SENS:POW:SWE:POW:STEP{}',
        get_parser= int,
        vals=vals.Numbers(10, 1000)  # *RST: 500
        )


        #Sets the stop level for the power versus power measurement

        self.add_parameter('stop_power_analysis',
        label='stop_power_analysis',
        get_cmd='SENS:POW:SWE:POW:STOP?',
        set_cmd='SENS:POW:SWE:POW:STOP{}',
        get_parser= float,
        vals=vals.Numbers(-145, 20)  # *RST: 40
        )



        #Selects the timing mode of the measurement

        self.add_parameter('timing_mode_powan',
        label='timing_mode_powan',
        get_cmd='SENS:POW:SWE:POW:TIM:MODE?',
        set_cmd='SENS:POW:SWE:POW:TIM:MODE{}',
        vals=vals.Enum("FAST","NORM","HPR","FAST","NORM")  # *RST: NORM
        )


        #Activates autoscaling of the Y axis of the diagram. Power mode

        self.add_parameter('y_pow_autoscale',
        label='y_pow_autoscale',
        get_cmd='SENS:POW:SWE:POW:YSC:AUTO?',
        set_cmd='SENS:POW:SWE:POW:YSC:AUTO{}',
        vals=vals.Enum("OFF","CEXP","FEXP","CFL","FFL")  #*RST: CEXPanding
        )

        #Resets the Y scale to suitable values after the use of auto scaling in the expanding mode.
        #Power mode

        self.add_parameter('y_pow_scale_rst',
        label='y_pow_scale_rst',
        get_cmd='SENS:POW:SWE:POW:YSC:AUTO:RES?',
        set_cmd='SENS:POW:SWE:POW:YSC:AUTO:RES{}',
        vals=vals.Enum()
        )

        #Sets the maximum value for the y axis of the measurement diagram. Power mode (dB)

        self.add_parameter('max_y_axis_powmode',
        label='max_y_axis_powmode',
        get_cmd='SENS:POW:SWE:POW:YSC:MAX?',
        set_cmd='SENS:POW:SWE:POW:YSC:MAX{}',
        get_parser=float,
        vals=vals.Numbers(-200,100) # increment: 0.01 ; *RST: 30
        )

        #Sets the minimum value for the y axis of the measurement diagram . Power mode (dB)

        self.add_parameter('min_y_axis_powmode',
        label='min_y_axis_powmode',
        get_cmd='SENS:POW:SWE:POW:YSC:MIN?',
        set_cmd='SENS:POW:SWE:POW:YSC:MIN{}',
        get_parser=float,
        vals=vals.Numbers(-200,100) # increment: 0.01 ; *RST: -40
        )


        #Selects single or continuous mode for power analysis (all measurement modes).

        self.add_parameter('power_analysis_mode',
        label='power_analysis_mode',
        get_cmd='SENS:POW:SWE:RMOD?',
        set_cmd='SENS:POW:SWE:RMOD{}',
        vals=vals.Enum("SING,CONT") # *RST: SING
        )


    #---------------------------Time measurement


        #Selects the averaging factor in time mode. The count number determines how many 
        #measurement cycles are used to form a measurement result. Higher averaging counts
        #reduce noise but increase the measurement time. Averaging requires a stable trigger
        #event so that the measurement cycles have the same timing. TIME MODE
        
        self.add_parameter('averaging_factor',
        label='averaging_factor',
        get_cmd='SENS:POW:SWE:TIME:AVER:COUN?',
        set_cmd='SENS:POW:SWE:TIME:AVER:COUN{}',
        vals=vals.Enum("1","2","4","8","16","32","64","128","256","512","1024") # *RST:1
        )


        #Generates a reference curve for "Time" measurement

        self.add_parameter('ref_curve_timemeas',
        label='ref_curve_timemeas',
        get_cmd='SENS:POW:SWE:TIME:REF:DATA:COPY?',
        set_cmd='SENS:POW:SWE:TIME:REF:DATA:COPY{}',
        vals=vals.Enum("") 
        )


        #Queries the number of points from the reference curve in "Time" measurement
        self.add_parameter('query_npoints_ref_curve_timemeas',
        label='query_npoints_ref_curve_timemeas',
        get_cmd='SENS:POW:SWE:TIME:REF:DATA:POIN?',
        set_cmd='SENS:POW:SWE:TIME:REF:DATA:POIN?{}',
        get_parser =int,
        vals=vals.Enum("")  #Range: 10 to 1000 ; *RST: 0
        )


        #Sets or queries the x values of the two reference points, i.e. "Time X (Point A)" and 
        #"Time X (Point B) "in "Time" measurement.

        self.add_parameter('x_set_time_meas',
        label='x_set_time_meas',
        get_cmd='SENS:POW:SWE:TIME:REF:DATA:XVAL?',
        set_cmd='SENS:POW:SWE:TIME:REF:DATA:XVAL{}',
        get_parser=str,
        vals=vals.Enum("")
        )


        #Sets or queries the y values of the two reference points, i.e. "Power Y (Point A)" and 
        #"Power Y (Point B)" in "Time" measurement
        self.add_parameter('y_set_time_meas',
        label='y_set_time_meas',
        get_cmd='SENS:POW:SWE:TIME:REF:DATA:YVAL?',
        set_cmd='SENS:POW:SWE:TIME:REF:DATA:YVAL{}',
        get_parser=str,
        vals=vals.Enum("")
        )

        #Selects single or continuous mode for measurement mode time in power analysis


        self.add_parameter('time_mode_poweran_set',
        label='time_mode_poweran_set',
        get_cmd='SENS:POW:SWE:TIME:RMOD?',
        set_cmd='SENS:POW:SWE:TIME:RMOD{}',
        vals=vals.Enum("SING", "CONT")  #*RST: CONT 
        )

        #Queries the sweep spacing for the power versus time measurement. The spacing is fixed to linear
        self.add_parameter('spacing_timean_set',
        label='spacing_timean_set',
        get_cmd='SENS:POW:SWE:TIME:SPAC:MODE?',
        set_cmd='SENS:POW:SWE:TIME:SPAC:MODE{}',
        vals=vals.Enum("LIN")  #*RST: LIN 
        )
 

        #Sets the start time for the power versus time measurement
        """
        Value 0 defines the trigger point. By choosing a negative time value, the trace can be shifted in the diagram. It is
        possible, that the measurement cannot be performed over the complete time range
        because of limitations due to sensor settings. In this case, an error message is output.
        """
        self.add_parameter('starttime_pow_vs_time',
        label='starttime_pow_vs_time',
        get_cmd='SENS:POW:SWE:TIME:STAR?',
        set_cmd='SENS:POW:SWE:TIME:STAR{}',
        get_parser=float,
        vals=vals.Numbers(-1, 1)  #Increment: 1E-12; *RST: -5E-6
        )


        #Sets the number of measurement steps for the power versus time measurement.
        #Value 0 defines the trigger point

        
        self.add_parameter('num_steps_pow_vs_time',
        label='num_steps_pow_vs_time',
        get_cmd='SENS:POW:SWE:TIME:STEP?',
        set_cmd='SENS:POW:SWE:TIME:STEP{}',
        get_parser=int,
        vals=vals.Numbers(10, 1000)  # *RST: 500
        )


        #Sets the stop time for the power versus time measurement.

        self.add_parameter('stoptime_pow_vs_time',
        label='stoptime_pow_vs_time',
        get_cmd='SENS:POW:SWE:TIME:STOP?',
        set_cmd='SENS:POW:SWE:TIME:STOP{}',
        get_parser=float,
        vals=vals.Numbers(0,2)  #Increment: 1E-12; *RST: 1E-3
        )

        #which trigger 
        """
        Determines, whether the measurement data processing starts with a trigger event in
        one of the sensors (Logical OR), or whether all channels have to be triggered (logical
        AND). Each sensor evaluates a trigger event according to its setting independently.
        This function supports the internal or external trigger modes with multi-channel time
        measurements.
        """
        self.add_parameter('which_trigger',
        label='which_trigger',
        get_cmd='SENS:POW:SWE:TIME:TEV?',
        set_cmd='SENS:POW:SWE:TIME:TEV{}',
        vals=vals.Enum("AND","OR")  #*RST: AND
        )


        #Activates autoscaling of the Y axis in the diagram time mode

        self.add_parameter('y_time_autoscale',
        label='y_time_autoscale',
        get_cmd='SENS:POW:SWE:TIME:YSC:AUTO?',
        set_cmd='SENS:POW:SWE:TIME:YSC:AUTO{}',
        vals=vals.Enum("OFF","CEXP","FEXP","CFL","FFL")  #*RST: CEXPanding
        )


        #Resets the Y scale to suitable values after the use of auto scaling in the expanding mode
        #time mode

        self.add_parameter('y_time_scale_rst',
        label='y_time_scale_rst',
        get_cmd='SENS:POW:SWE:TIME:YSC:AUTO:RES?',
        set_cmd='SENS:POW:SWE:TIME:YSC:AUTO:RES{}',
        vals=vals.Enum()
        )

        #Sets the maximum value for the y axis of the measurement diagram. Time mode (dBm)
        self.add_parameter('max_y_axis_timemode',
        label='max_y_axis_timemode',
        get_cmd='SENS:POW:SWE:TIME:YSC:MAX?',
        set_cmd='SENS:POW:SWE:TIME:YSC:MAX{}',
        get_parser=float,
        vals=vals.Numbers(-200,100) # increment: 0.01 ; *RST: 30
        )

        #Sets the minimum value for the y axis of the measurement diagram. Time mode (dBm)
        self.add_parameter('min_y_axis_timemode',
        label='min_y_axis_timemode',
        get_cmd='SENS:POW:SWE:TIME:YSC:MIN?',
        set_cmd='SENS:POW:SWE:TIME:YSC:MIN{}',
        get_parser=float,
        vals=vals.Numbers(-200,100) # increment: 0.01 ; *RST: not specified 
        )

        #------------------------------------------- End of SENSe SWEep Subsystem


        #SOURce Subsystem. The SOURce subsystem contains 
        #the commands for configuring the digital and analog signals.

        #The command in this subsytem allows you to disable all active modulations at once, 
        # and, vice versa, to restore the last active ones.

        self.add_parameter('all_modulation_state',
        label='all_modulation_state',
        get_cmd='SOUR:MOD:ALL:STAT?', #not sure 
        set_cmd='SOUR:MOD:ALL:STAT{}',
        vals=vals.Enum("0","1","OFF","ON") # ; *RST: 0 
        )

        #SOURce:AM Subsystem. AM subsystem contains the commands for setting the amplitude modulation
        #and also the broadband amplitude modulation.

        #Activates amplitude modulation.
        self.add_parameter('modulation_state',
        label='modulation_state',
        get_cmd='SOUR:AM{channum}:STAT?',  
        set_cmd='SOUR:AM{channum}:STAT{}',
        vals=vals.Enum("0","1","OFF","ON") # ; *RST: 0 
        )


        #Selects the modulation source for amplitude modulation
        """
        LF1|LF2
        Uses an internally generated LF signal.
        EXT1|EXT2
        Uses an externally supplied LF signal.
        NOISe
        Uses the internally generated noise signal.
        INTernal
        Uses the internally generated signal of LF1.
        EXTernal
        Uses an external LF signal (EXT1).
        
        """

        self.add_parameter('modulation_source_amp',
        label='modulation_source_amp',
        get_cmd='SOUR:AM{channum}:SOUR?',  
        set_cmd='SOUR:AM{channum}:SOUR{}',
        vals=vals.Enum("LF1","LF2","NOIS ","EXT1","EXT2","EXT","INT") #  *RST: LF1 <AM1>; LF2 <AM2>
        )


        #Sets the depth of the amplitude modulation in percent.

        self.add_parameter('perc_amp_modulation',
        label='perc_amp_modulation',
        get_cmd='SOUR:AM{channum}:DEPT?',  
        set_cmd='SOUR:AM{channum}:DEPT{}',
        get_parser=float,
        vals=vals.Numbers(0,100) #Increment: 0.01; *RST: 30
        )


        #Sets the depth of the linear amplitude modulation in percent / volt.

        self.add_parameter('perc_lin_amp_modulation',
        label='perc_lin_amp_modulation',
        get_cmd='SOUR:AM:DEPTh:LIN?',  
        set_cmd='SOUR:AM:DEPTh:LIN{}',
        get_parser=float,
        vals=vals.Numbers(0,100) #Increment: 0.01; *RST: 30
        )

        #Sets the depth of the exponential amplitude modulation in dB/volt.

        self.add_parameter('perc_exp_amp_modulation',
        label='perc_exp_amp_modulation',
        get_cmd='SOUR:AM{channum}:DEPT:EXP?',  
        set_cmd='SOUR:AM{channum}:DEPT:EXP{}',
        get_parser=float,
        vals=vals.Numbers(0,100) #Increment: 0.01; *RST: 10
        )

        #Selects the mode of the amplitude modulation.
        self.add_parameter('amp_modulation_mode',
        label='amp_modulation_mode',
        get_cmd='SOUR:AM:MODE?',  
        set_cmd='SOUR:AM:MODE{}',
        vals=vals.Enum("SCAN","NORM") #*RST: NORM
        )

        #Sets the total depth of the LF signal when using combined
        #signal sources in amplitude modulation.

        self.add_parameter('depth_LF_signal',
        label='depth_LF_signal',
        get_cmd='SOUR:AM:DEPT:SUM?',  
        set_cmd='SOUR:AM:DEPT:SUM{}',
        get_parser = float,
        vals=vals.Numbers(0,100) # Increment: 0.01 ; *RST:30
            
        )

        #Selects the coupling mode. The coupling mode parameter also determines the mode
        #for fixing the total depth.
        """
        UNCoupled
        Does not couple the LF signals.
        The deviation depth values of both paths are independent.
        TOTal
        Couples the deviation depth of both paths.
        RATio
        Couples the deviation depth ratio of both paths
        
        """

        self.add_parameter('coupling_mode',
        label='coupling_mode',
        get_cmd='SOUR:AM:DEV:MODE?',  
        set_cmd='SOUR:AM:DEV:MODE{}',
        vals=vals.Enum("UNC","TOT" ,"RAT") # *RST:UNC
            
        )

        #Sets the deviation ratio (path#2 to path#1) in percent
        self.add_parameter('dev_ratio',
        label='dev_ratio',
        get_cmd='SOUR:AM:RAT?',  
        set_cmd='SOUR:AM:RAT{}',
        get_parser = float,
        vals=vals.Numbers(0,100) # *Increment: 0.01 ; *RST: 100
            
        )

        #For [:SOURce<hw>]:AM:TYPEEXP, sets the sensitivity of 
        # the external signal source for amplitude modulation
        self.add_parameter('sensitivity_exp_ext_sign',
        label='sensitivity_exp_ext_sign',
        get_cmd='SOUR:AM{channum}:SENS:EXP?',  
        set_cmd='SOUR:AM{channum}:SENS:EXP{}',
        get_parser = float,
        vals=vals.Numbers(0,100) # Increment: 0.01 ; *RST: 10
            
        )

        #For [:SOURce<hw>]:AM:TYPE LIN, sets the sensitivity of the external signal source 
        # for amplitude modulation

        self.add_parameter('sensitivity_lin_ext_sign',
        label='sensitivity_lin_ext_sign',
        get_cmd='SOUR:AM{channum}:SENS:LIN?',  
        set_cmd='SOUR:AM{channum}:SENS:LIN{}',
        get_parser = float,
        vals=vals.Numbers(0,100) # Increment: 0.01 ; *RST: 30
            
        )

        #Selects the type of amplitude modulation. 

        self.add_parameter('amp_modulation_mode',
        label='amp_modulation_mode',
        get_cmd='SOUR:AM:TYPE?',  
        set_cmd='SOUR:AM:TYPE{}',
        vals=vals.Enum("LIN","EXP") #*RST: LIN
            
        )

        #SOURce:FM Subsystem. The FM subsystem contains
        #the commands for setting the frequency modulation

        #Activates frequency modulation.

        self.add_parameter('freq_modulation_state',
        label='freq_modulation_state',
        get_cmd='SOUR:FM{channum}:STAT?',  
        set_cmd='SOUR:FM{channum}:STAT{}',
        vals=vals.Enum("0","1","OFF","ON") # ; *RST: 0 
        )

        #Sets the modulation deviation of the frequency modulation in Hz.
        MAX_VALUE= 10_000 #guarda bene datasheet
        self.add_parameter('dev_freq_modulation',
        label='dev_freq_modulation',
        get_cmd='SOUR:FM{channum}:DEV?',  
        set_cmd='SOUR:FM{channum}:DEV{}',
        get_parser=float,
        vals=vals.Numbers(0, MAX_VALUE) # increment = 0.01 ; *RST: *RST: 1E3
        )

        #Selects the modulation source for frequency modulation.
        """
        LF1|LF2
        Uses an internally generated LF signal.
        INTernal = LF1
        Works like LF1
        EXTernal
        Works like EXT1
        EXT1|EXT2
        Uses an externally supplied LF signal.
        NOISe
        Uses the internally generated noise signal.
        *RST: LF1 <FM1>; LF2 <FM2>
        """


        self.add_parameter('modulation_source_freq',
        label='modulation_source_freq',
        get_cmd='SOUR:FM{channum}:SOUR?',  
        set_cmd='SOUR:FM{channum}:SOUR{}',
        vals=vals.Enum("LF1","LF2","NOIS ","EXT1","EXT2","EXT","INT") #  *RST: LF1 <AM1>; LF2 <AM2>
        )

        #Selects the coupling mode. The coupling mode parameter also determines the mode 
        #for fixing the total deviation
        """
        UNCoupled
        Does not couple the LF signals.
        The deviation values of both paths are independent.
        TOTal
        Couples the deviation of both paths.
        RATio
        Couples the deviation ratio of both paths
        """
        self.add_parameter('freq_coupling_mode',
        label='freq_coupling_mode',
        get_cmd='SOUR:FM:DEV:MODE?',  
        set_cmd='SOUR:FM:DEV:MODE{}',
        vals=vals.Enum("UNC","TOT","RAT") # ; *RST: UNC  
        )

        #Sets the total deviation of the LF signal when using combined signal 
        #sources in frequency modulation.
        self.add_parameter('freq_total_dev',
        label='freq_total_dev',
        get_cmd='SOUR:FM:DEV:SUM?',  
        set_cmd='SOUR:FM:DEV:SUM{}',
        get_parser = float, 
        vals=vals.Numbers(0, 40e6) # Increment: 0.01 ; *RST: 1E3 
        )



        #Sets the deviation ratio (path2 to path1) in percent.
        self.add_parameter('freq_dev_ratio',
        label='freq_dev_ratio',
        get_cmd='SOUR:FM:RAT?',  
        set_cmd='SOUR:FM:RAT{}',
        get_parser=float,
        vals=vals.Numbers(0,100) # Increment: 0.01 ; *RST: 100  
        )


        #Selects the mode for the frequency modulation.

        """
        HBANdwidth
        Selects maximum range for modulation bandwidth.
        LNOise
        Selects optimized phase noise and spurious characteristics with
        reduced modulation bandwidth and FM deviation.
        
        """

        self.add_parameter('freq_modulation_mode',
        label='freq_modulation_mode',
        get_cmd='SOUR:FM:MODE?',  
        set_cmd='SOUR:FM:MODE{}',
        vals=vals.Enum("HBAN" ,"LNO") # ; *RST: HBAN  
        )

        #Queries the sensitivity of the externally supplied signal for frequency modulation.
        #The sensitivity depends on the set modulation deviation. Sensitivity in Hz/V. 
        #It is assigned to the voltage value for full modulation of the input 
        """
        Range: 0 to max
        Increment: 0.01
        """

        self.add_parameter('query_sens_signal',
        label='query_sens_signal',
        get_cmd='SOUR:FM:SENS?',  
        set_cmd='SOUR:FM:SENS?{}',
        get_parser=float, 
        vals=vals.Enum("") 
        )

        #SOURce:PM Subsystem. 
        #The PM subsystem contains the commands for setting the phase modulation.

        #Activates phase modulation.
        self.add_parameter('phase_modulation_state',
        label='phase_modulation_state',
        get_cmd='SOUR:PM{channum}:STAT?',  
        set_cmd='SOUR:PM{channum}:STAT{}',
        vals=vals.Enum("ON" ,"OFF","1","0") # ; *RST: 0  
        )

        #Selects the modulation source for phase modulation signal.

        """
        LF1|LF2
        Uses an internally generated LF signal.
        EXT1|EXT2
        Uses an externally supplied LF signal.
        NOISe
        Uses the internally generated noise signal.
        INTernal
        Uses the internally generated signal of LF1.
        EXTernal
        Uses an external LF signal (EXT1).
        *RST: LF1 <PM1>; LF2 <PM2>
        
        """
        self.add_parameter('modulation_source_phase',
        label='modulation_source_phase',
        get_cmd='SOUR:PM{channum}:SOUR?',  
        set_cmd='SOUR:PM{channum}:SOUR{}',
        vals=vals.Enum("LF1","LF2","NOIS ","EXT1","EXT2","EXT","INT") #  *RST: LF1 <AM1>; LF2 <AM2>
        )

        #Selects the mode for the phase modulation.
        """
        HBANdwidth
        Sets the maximum available bandwidth.
        HDEViation
        Sets the maximum range for ΦM deviation.
        LNOise
        Selects a phase modulation mode with phase noise and spurious
        characteristics close to CW mode.
        *RST: HBANdwidth

        """

        self.add_parameter('phase_modulation_mode',
        label='phase_modulation_mode',
        get_cmd='SOUR:PM:MODE?',  
        set_cmd='SOUR:PM:MODE{}',
        vals=vals.Enum("HBAN" ,"LNO","HDEV") # ; *RST: HBAN  
        )

        #Selects the coupling mode. The coupling mode parameter also determines the mode 
        #for fixing the total deviation.
        self.add_parameter('phase_coupling_mode',
        label='phase_coupling_mode',
        get_cmd='SOUR:PM:DEV:MODE?',  
        set_cmd='SOUR:PM:DEV:MODE{}',
        vals=vals.Enum("UNC","TOT","RAT") # ; *RST: UNC  
        )

        #Sets the total deviation of the LF signal when using combined signal
        #sources in phase modulation.
        self.add_parameter('phase_total_dev',
        label='phase_total_dev',
        get_cmd='SOUR:PM:DEV:SUM?',  
        set_cmd='SOUR:PM:DEV:SUM{}',
        get_parser = float, 
        vals=vals.Numbers(0, 20) # Increment: 1E-6  ; *RST: 1
        )

        #Sets the deviation ratio (path2 to path1) in percent.

        self.add_parameter('phase_dev_ratio',
        label='phase_dev_ratio',
        get_cmd='SOUR:PM:RAT?',  
        set_cmd='SOUR:PM:RAT{}',
        get_parser=float,
        vals=vals.Numbers(0,100) # Increment: 0.01 ; *RST: 100  
        )
        

        #Queries the sensitivity of the externally applied signal for phase modulation.
        #The returned value reports the sensitivity in RAD/V. 
        #It is assigned to the voltage value for full modulation of the input.

        self.add_parameter('query_sens_signal_phase',
                            label='query_sens_signal_phase',
                            get_cmd='SOUR:PM:SENS?',  
                            set_cmd='SOUR:PM:SENS?{}',
                            get_parser=float, 
                            vals=vals.Enum("") 
        )


        #Sets the modulation deviation of the phase modulation in RAD
        MAXVALUE_P= 2
        self.add_parameter('phase_mod_dev_rad',
                            label='phase_mod_dev_rad',
                            get_cmd='SOUR:PM{channum}:DEV?',  
                            set_cmd='SOUR:PM{channum}:DEV?{}',
                            get_parser=float, 
                            vals=vals.Numbers(0,MAXVALUE_P) #Increment: 1, *RST: 1 
        )


        #SOURce:PULM Subsystem.
        #The PULM subsystem contains the commands for setting the pulse modulation

        #Selects the mode for the pulse modulation

        """
        SINGle
        Generates a single pulse.
        DOUBle
        Generates two pulses within one pulse period.
        PTRain
        Generates a user-defined pulse train.
        Specify the pulse sequence with the commands:
        [:SOURce<hw>]:PULM:TRAin:ONTime
        [:SOURce<hw>]:PULM:TRAin:OFFTime
        [:SOURce<hw>]:PULM:TRAin:REPetition

        """

        self.add_parameter('pulse_modulation_mode',
                            label='pulse_modulation_mode',
                            get_cmd='SOUR:PULM:MODE?',  
                            set_cmd='SOUR:PULM:MODE{}',
                            vals=vals.Enum("SING", "DOUB" ,"PTR") # ; *RST: SING
        )


        

        #Selects a trigger mode - auto, single, external, external single or external gated - 
        #for generating the modulation signal

        self.add_parameter('pulse_mod_trg_mode',
                            label='pulse_mod_trg_mode',
                            get_cmd='SOUR:PULM:TRIG:MODE?',  
                            set_cmd='SOUR:PULM:TRIG:MODE{}',
                            vals=vals.Enum("AUTO","EXT","EGAT","ING","ESIN") # ; *RST: AUTO
        )


        
        #Activates pulse modulation
        self.add_parameter('pulsemod_state',
                           label='Pulse Modulation',
                           get_cmd='SOUR:PULM:STAT?',
                           set_cmd='SOUR:PULM:STAT{}',
                           val_mapping=create_on_off_val_mapping(on_val='1',
                                                               off_val='0')
                            
                            )
        
        ##Selects the source for pulse modulation. Parms: INTernal | EXTernal       
        self.add_parameter('pulsemod_source',
                           label='Pulse Modulation Source',
                           get_cmd='SOUR:PULM:SOUR?',
                           set_cmd='SOUR:PULM:SOUR{}',
                           vals=vals.Enum('INT', 'EXT', 'int', 'ext'))
        
         
        
        #Sets the polarity of the pulse modulator signal. 
        #This command is effective only for an external modulation signal.
        #Parms: NORMal | INVerted
        self.add_parameter('pulse_pol',
                           label='pulse_polarity',
                           get_cmd='SOUR:PULM:POL?',
                           set_cmd='SOUR:PULM:POL{}',
                           get_parser=float,
                           ) 

       
        #Sets the width of the generated pulse. The width determines the pulse length.
        #The pulse width must be at least 20ns less than the set pulse period
        self.add_parameter('pulse_width',
                           label='pulse_width',
                           get_cmd='SOUR:PULM:WIDT?',
                           set_cmd='SOUR:PULM:WIDT{:.2f}',
                           get_parser=float,
                           vals=vals.Numbers(20,100),
                           ) #20ns to 100 s, increment: 10 ns 
                                                        

        #Sets the impedance for the external pulse trigger and pulse modulation input.
        self.add_parameter('pulse_imp',
                           label='pulse_impedance ',
                           get_cmd='SOUR:PULM:IMP?',
                           set_cmd='SOUR:PULM:IMP{:.2f}',
                           vals=vals.Enum('G50','G10K'),
                           )

        
        #Sets the period of the generated pulse, that means the repetition frequency of the internally generated modulation signal.
        self.add_parameter('pulse_period',
                           label='pulse period modulated signal',
                           get_cmd='SOUR:PULM:PER?',
                           set_cmd='SOUR:PULM:PER{}',
                           vals=vals.Numbers(20e-9, 100)  #Increment: 5E-9 ; *RST: 10E-6 
                            )

        #Sets the pulse delay
        self.add_parameter('pulse_delay',
                           label='pulse delay modulated signal',
                           get_cmd='SOUR:PULM:DEL?',
                           set_cmd='SOUR:PULM:DEL{}',
                           get_parser = float,
                           vals=vals.Numbers()  #*RST: 1ms 
                            )
        
        #Sets the delay from the start of the first pulse to the start of the second pulse

        self.add_parameter('pulse_double_delay',
                           label='pulse double delay modulated signal',
                           get_cmd='SOUR:PULM:DOUB:DEL?',
                           set_cmd='SOUR:PULM:DOUB:DEL{}',
                           get_parser = float,
                           vals=vals.Numbers()  #*RST: 1e-6 
                            )
        #Sets the width of the second pulse
        self.add_parameter('double_pulse_width',
                           label='double pulse width modulated signal',
                           get_cmd='SOUR:PULM:DOUB:WIDT?',
                           set_cmd='SOUR:PULM:DOUB:WIDT{}',
                           get_parser = float,
                           vals=vals.Numbers()  #*Increment: 5E-9 
                            )

        #Provided for backward compatibility with former Rohde & Schwarz signal generators.
        #Works like the command [:SOURce<hw>]:PULM:MODE DOUBle.

        self.add_parameter('double_pulse_width_RS',
                           label='double pulse width modulated signal',
                           get_cmd='SOUR:PULM:DOUB:STAT?',
                           set_cmd='SOUR:PULM:DOUB:STAT{}',
                           vals=vals.Enum('0','1','OFF','ON')  #*RST: 0
                            )
        #Sets the transition mode for the pulse signal.
        """
        SMOothed
        flattens the slew rate, resulting in longer rise/fall times.
        FAST
        enables fast transitions with shortest rise and fall times
        """

        self.add_parameter('set_transition_mode',
                           label='set_transition_mode',
                           get_cmd='SOUR:PULM:TTYP?',
                           set_cmd='SOUR:PULM:TTYP{}',
                           vals=vals.Enum('SMO','FAST')  #*RST: FAST
                            )

        #Sets the threshold for the input signal at the [Pulse Ext] connector.
        self.add_parameter('set_ipt_thr',
                           label='set_ipt_thr',
                           get_cmd='SOUR:PULM:THR?',
                           set_cmd='SOUR:PULM:THR{}',
                           get_parser=float,
                           vals=vals.Numbers(0,2)  #Increment: 0.1 ; *RST: 1 ; Default unit: V
                            )


        #If [:SOURce<hw>]:PULM:TRIGger:MODE SINGle, triggers the pulse generator
        self.add_parameter('pulse_mod_trg_gen',
                            label='pulse_mod_trg_gen',
                            get_cmd='SOUR:PULM:INT:TRA:TRIG:IMM?',  
                            set_cmd='SOUR:PULM:INT:TRA:TRIG:IMM{}',
                            vals=vals.Enum("") # ; *RST: AUTO
        )

        #if trig_pulm_mode : SIN -> generate a single trigger with the next param
        self.add_parameter('trig_pulm_mode',
                           label='trigger when in pulse modulation mode',
                           get_cmd='SOUR:PULM:INT:TRA:TRIG?',
                           set_cmd='SOUR:PULM:INT:TRA:TRIG{}',
                           vals=vals.Enum('IMM',)
                            )


        #Source Pulse Train 

        #Queries the available pulse train files in the specified directory
        self.add_parameter('query_pulse_train',
                        label='query_pulse_train',
                        get_cmd='SOUR:PULM:TRA:CAT?',
                        set_cmd='SOUR:PULM:TRA:CAT?{}',
                        vals=vals.Enum()
                            )
        #Deletes the specified pulse train file.
        self.add_parameter('delete_pulse_train',
                        label='delete_pulse_train',
                        get_cmd='SOUR:PULM:TRA:DEL?',
                        set_cmd='SOUR:PULM:TRA:DEL?{}',
                        get_parser=str,
                        vals=vals.Enum()
                            )
        
        #Enters the pulse on/off times values in the selected list.

        """
        
        <OffTime> Offtime#1{, Offtime#2, ...} | binary block data
        List of comma-separated numeric values or binary block data,
        where:
        The list of numbers can be of any length.
        In binary block format, 8 (4) bytes are always interpreted as a
        floating-point number with double accuracy.
        See :FORMat[:DATA] on page 444 for details.
        The maximum length is 2047 values.
        Range: 0 ns to 5 ms
        
        
        """
        self.add_parameter('delete_pulse_train',
                        label='delete_pulse_train',
                        get_cmd='SOUR:PULM:TRA:ONT?',
                        set_cmd='SOUR:PULM:TRA:ONT?{}',
                        get_parser=str,
                        vals=vals.Enum()
                            )
        
        self.add_parameter('delete_pulse_train',
                        label='delete_pulse_train',
                        get_cmd='SOUR:PULM:TRA:OFFT?',
                        set_cmd='SOUR:PULM:TRA:OFFT?{}',
                        get_parser=str,
                        vals=vals.Enum()
                            )
        

        #Queries the number of on and off time entries and repetitions in the selected list.

        self.add_parameter('number_rep_points',
                        label='number_rep_points',
                        get_cmd='SOUR:PULM:TRA:REP:POIN?',
                        set_cmd='SOUR:PULM:TRA:REP:POIN?{}',
                        vals=vals.Enum()
                            )

        self.add_parameter('number_on_rep_points',
                        label='number_on_rep_points',
                        get_cmd='SOUR:PULM:TRA:ONT:POIN?',
                        set_cmd='SOUR:PULM:TRA:ONT:POIN?{}',
                        get_parser=int,
                        vals=vals.Enum()  #Range: 0 to INT_MAX; *RST: 0
                            )
        self.add_parameter('number_off_rep_points',
                        label='number_off_rep_points',
                        get_cmd='SOUR:PULM:TRA:OFFT:POIN?',
                        set_cmd='SOUR:PULM:TRA:OFFT:POIN?{}',
                        get_parser=int,
                        vals=vals.Enum()  #Range: 0 to INT_MAX; *RST: 0
                            )

        #Sets the number of repetitions for each pulse on/off time value pair

        self.add_parameter('number_reps_one_pulse',
                        label='number_reps_one_pulse',
                        get_cmd='SOUR:PULM:TRA:REP?',
                        set_cmd='SOUR:PULM:TRA:REP?{}',
                        get_parser=int,
                        vals=vals.Enum(0, 65535)  
                            )

        #Selects or creates a data list in pulse train mode. 
        #If the list with the selected name does not exist, a new list is created.

        self.add_parameter('number_reps_one_pulse',
                        label='number_reps_one_pulse',
                        get_cmd='SOUR:PULM:TRA:SEL?',
                        set_cmd='SOUR:PULM:TRA:SEL?{}',
                        get_parser=str,
                        vals=vals.Enum()  
                            )

        #noise generator

        #Sets the noise level in the system bandwidth when bandwidth limitation is enabled
        self.add_parameter('set_noise_lvl',
                        label='set_noise_lvl',
                        get_cmd='SOUR:NOIS:BAND?',
                        set_cmd='SOUR:NOIS:BAND{}',
                        get_parser=float,
                        vals=vals.Numbers(100e3,10e6)   #Increment: 100E3,*RST: 100E3
                            )

        #Activates noise bandwidth limitation
        self.add_parameter('bwd_limitation',
                        label='bwd_limitation',
                        get_cmd='SOUR:NOIS:BAND?',
                        set_cmd='SOUR:NOIS:BAN{}',
                        vals=vals.Enum('0','1','ON','OFF')   #*RST: 0
                            )
        
        #Sets the distribution of the noise power density.
        self.add_parameter('noise_power_density',
                        label='noise_power_density',
                        get_cmd='SOUR:NOIS:DIST?',
                        set_cmd='SOUR:NOIS:DIST{}',
                        vals=vals.Enum('GAUS','EQU')   #*RST: 0
                            )
        #Queries the level of the noise signal per Hz in the total bandwidth.
        self.add_parameter('query_noise_level_total',
                        label='query_noise_level_total',
                        get_cmd='SOUR:NOIS:LEV:REL?',
                        set_cmd='SOUR:NOIS:LEV:REL{}',
                        get_parser=float,
                        vals=vals.Numbers(-149.18, -52.67)   #*Increment: 0.1 ; *RST: -69.84
                            )
        
        #Queries the level of the noise signal in the system bandwidth within
        #the enabled bandwidth limitation

        self.add_parameter('query_noise_level_enabled',
                        label='query_noise_level_enabled',
                        get_cmd='SOUR:NOIS:LEV:REL?',
                        set_cmd='SOUR:NOIS:LEV:REL{}',
                        get_parser=float,
                        vals=vals.Numbers()   #*RST: 3.84 MHz
                            )


        #SOURce:PGEN Subsystem. The PGEN subsystem contains the commands for setting 
        #output of the pulse modulation signal

        #Sets the polarity of the pulse output signal.
        """
        NORMal
        Outputs the pulse signal during the pulse width, that means during
        the high state.
        INVerted
        Inverts the pulse output signal polarity. The pulse output signal is
        suppressed during the pulse width, but provided during the low
        state.
        *RST: NORMal
        """
        self.add_parameter('pulse_output_pol',
                        label='pulse_output_pol',
                        get_cmd='SOUR:PGEN:OUTP:POL?',
                        set_cmd='SOUR:PGEN:OUTP:POL{}',
                        vals=vals.Enum('NORM','INV')   #*RST: 3.84 MHz
                            )

        #Activates the output of the pulse modulation signal.
        self.add_parameter('pulse_output_state',
                        label='pulse_output_state',
                        get_cmd='SOUR:PGEN:OUTP:STAT?',
                        set_cmd='SOUR:PGEN:OUTP:STAT{}',
                        vals=vals.Enum('0','1','ON','OFF')   #*RST: 0
                            )
        
        #Enables the output of the video/sync signal
        self.add_parameter('video_signal_out_state',
                        label='video_signal_out_state',
                        get_cmd='SOUR:PGEN:STAT?',
                        set_cmd='SOUR:PGEN:STAT{}',
                        vals=vals.Enum('0','1','ON','OFF')   #*RST: 0
                            )

        #SOURce:PHASe Subsystem. This subsystem contains the commands for adjusting the phase of the RF output 
        #signal relative to a reference signal of the same frequency 

        #Sets the phase variation relative to the current phase
        self.add_parameter('phase_var',
                        label='phase_var',
                        get_cmd='SOUR:PHAS?',
                        set_cmd='SOUR:PHAS{}',
                        get_parser=float,
                        vals=vals.Numbers(-36000,36000)   #ncrement: 0.001, *RST: 0 , Default unit: DEG
                            )

        #Assigns the value set with command [:SOURce<hw>]:PHASe as the reference phase.
        self.add_parameter('phase_var_set',
                        label='phase_var_set',
                        get_cmd='SOUR:PHAS:REF?',
                        set_cmd='SOUR:PHAS:REF{}',
                        vals=vals.Numbers()   #ncrement: 0.001, *RST: 0 , Default unit: DEG
                            )


        #SOURce:POWer Subsystem. The SOURce:POWer subsystem contains the commands for setting the output level, 
        #level control and level correction of the RF signal. The default units are dBm.

        #Adjusts the output level to the operating conditions

        """
        AUTO
        Adjusts the output level to the operating conditions automatically.
        1|ON
        Activates internal level control permanently.
        OFFTable
        Controls the level using attenuation values of the internal ALC
        table.
        0|OFF
        Provided only for backward compatibility with other
        Rohde & Schwarz signal generators.
        The R&S SMA100B accepts these values and maps them automatically
        as follows:
        0|OFF = OFFTable
        ONTable
        Starts with the attenuation setting from the table and continues
        with automatic level control.
                
        """
        self.add_parameter('output_level_adj',
                        label='output_level_adj',
                        get_cmd='SOUR:POW:ALC:STAT?',
                        set_cmd='SOUR:POW:ALC:STAT{}',
                        vals=vals.Enum('0','OFF','AUTO','1','ON','ONT','PRES','OFFT') # *RST: AUTO
                                 )
        

        #Sets the sensitivity of the ALC detector.
        """
        AUTO
        Selects the optimum sensitivity automatically.
        FIXed
        Fixes the internal level detector.
        """

        self.add_parameter('ALC_sensitivity',
                        label='ALC_sensitivity',
                        get_cmd='SOUR:POW:ALC:DSEN?',
                        set_cmd='SOUR:POW:ALC:DSEN{}',
                        vals=vals.Enum('AUTO','FIX') # *RST: AUTO
                                 )
        
        #Activates level control for correction purposes temporarily

        """
        POW:ALC OFF
        Deactivates automatic level control at the RF output.
        POW:ALC:SONC
        Executes level control (once).
        
        """

        self.add_parameter('ctrl_lvl_temp_state',
                        label='ctrl_lvl_temp_state',
                        get_cmd='SOUR:POW:ALC:SONC?',
                        set_cmd='SOUR:POW:ALC:SONC{}',
                        vals=vals.Enum('OFF','SONC') # *RST: AUTO
                                 )

        #Selects the type of step attenuator used below 20 GHz
        """
        MECHanical
        Uses the mechanical step attenuator over the all frequencies.
        ELECtronic
        Uses the electronic step attenuator up to 20 GHz
        
        """

        self.add_parameter('step_attenuator_low',
                        label='step_attenuator_low',
                        get_cmd='SOUR:POW:ATT:PATT?',
                        set_cmd='SOUR:POW:ATT:PATT{}',
                        vals=vals.Enum('MECH','ELEC') # *RST: AUTO
                                 )


        #Selects the state the attenuator is to assume if the RF signal is switched off
        """
        FATTenuation
        The step attenuator switches to maximum attenuation
        UNCHanged
        Retains the current setting and keeps the output impedance
        constant during RF off.
        *RST: n.a. (factory preset: FATTenuation)
        
        """


        self.add_parameter('attenuator_state',
                        label='attenuator_state',
                        get_cmd='SOUR:POW:ATT:RFOF:MODE?',
                        set_cmd='SOUR:POW:ATT:RFOF:MODE{}',
                        vals=vals.Enum('UNCH','FATT') # *RST: AUTO
                                 )

        #Displays the signal level as voltage of the EMF. The displayed value represents the 
        #voltage over a 50 Ohm load.

        self.add_parameter('signal_lvl_display',
                        label='signal_lvl_display',
                        get_cmd='SOUR:POW:EMF:STAT?',
                        set_cmd='SOUR:POW:EMF:STAT{}',
                        vals=vals.Enum('1','0','ON','OFF') # *RST: n.a. (factory preset: 0)
                                 )
        

        #level behaviour set
        """
        UNINterrupted|MONotone
        Uninterrupted level settings and strictly monotone modes.
        CVSWr
        Constant VSWR
        HDUN
        High dynamic uninterrupted level settings.
        
        """

        self.add_parameter('lvl_beah_set',
                        label='lvl_beah_set',
                        get_cmd='SOUR:POW:LBEH?',
                        set_cmd='SOUR:POW:LBEH{}',
                        vals=vals.Enum('AUTO','UNIN','MON','CVSW','HDUN') # *RST: AUTO
                                 )
        
        #Limits the maximum RF output level in CW and sweep mode.
        self.add_parameter('max_RF_output',
                        label='max_RF_output',
                        get_cmd='SOUR:POW:LIM:AMPL?',
                        set_cmd='SOUR:POW:LIM:AMPL{}',
                        get_parser=float,
                        vals=vals.Numbers() # Range: depends on the installed options ; 
                                            #Increment: 0.01; *RST: n.a. (factory preset: 30)
                                 )
        
        #Sets the RF level mode

        """
        NORMal
        Supplies the RF signal with the standard power level of the
        instrument.
        LOWNoise
        Supplies a very low noise sinewave signal.
        LOWDistortion
        Supplies a very pure sinewave signal.
        
        """
        self.add_parameter('RF_lvl_mode',
                        label='RF_lvl_mode',
                        get_cmd='SOUR:POW:LMOD?',
                        set_cmd='SOUR:POW:LMOD{}',
                        vals=vals.Enum('NORM','LOWN','LOWD') # *RST: NORMal  
                                 )
        
        #Sets the level for the subsequent sweep step if SWE:POW:MODE MAN.

        """
        
        You can select any level within the setting range, where:
        STARt is set with [:SOURce<hw>]:POWer:STARt
        STOP is set with [:SOURce<hw>]:POWer:STOP
        OFFSet is set with [:SOURce<hw>]:POWer[:LEVel][:IMMediate]:OFFSet

        all defined above
        
        """
        #Range: (STARt + OFFSet) to (STOP + OFFSet); Increment: 0.01 ; Default unit: dBm
        self.add_parameter('sweep_lvl',
                        label='sweep_lvl',
                        get_cmd='SOUR:POW:MAN?',
                        set_cmd='SOUR:POW:MAN{}',
                        get_parser=float,
                        vals=vals.Numbers() #  
                                 )
        
        #Selects the operating mode of the instrument to set the output level
        """
        CW|FIXed
        Operates at a constant level.
        CW and FIXed are synonyms.
        SWEep
        Sets sweep mode.

       """

        self.add_parameter('inst_operating_mode',
                        label='inst_operating_mode',
                        get_cmd='SOUR:POW:MODE?',
                        set_cmd='SOUR:POW:MODE{}',
                        vals=vals.Enum('CW','FIX','SWE') #  *RST: CW
                                 )
        

        #Sets the level at the RF output connector,without level offset. This value does not consider a specified offset. 

        self.add_parameter('inst_operating_mode',
                        label='inst_operating_mode',
                        get_cmd='SOUR:POW:POW?',
                        set_cmd='SOUR:POW:POW{}',
                        get_parser=float,
                        vals=vals.Numbers() #  Range: See data sheet ; Increment: 0.01, Default unit: dBm
                                 )


        #Sets the RF start/stop level in sweep mode
        """
        Sets the setting range calculated as follows:
        (Level_min + OFFSet) to (Level_max + OFFSet)
        Where the values are set with the commands:
        [:SOURce<hw>]:POWer[:LEVel][:IMMediate]:OFFSet
        [:SOURce<hw>]:POWer:STARt
        [:SOURce<hw>]:POWer:STOP
        Range: Minimum level to maximum level
        *RST: -30 (Start)/ -10 (Stop)
        Default unit: dBm
        
        """

        self.add_parameter('RF_lvl_start',
                        label='RF_lvl_start',
                        get_cmd='SOUR:POW:POW:STAR?',
                        set_cmd='SOUR:POW:POW{}',
                        get_parser=float,
                        vals=vals.Numbers() # RST: -30
                                 )

        self.add_parameter('RF_lvl_stop',
                        label='RF_lvl_stop',
                        get_cmd='SOUR:POW:POW:STOP?',
                        set_cmd='SOUR:POW:POW:STOP{}',
                        get_parser=float,
                        vals=vals.Numbers() # RST: -10
                                 )
        
        #Defines the type of step width to vary the RF output power step-by-step with the commands
        """
        DECimal
        Increases or decreases the level in steps of ten.
        USER
        Increases or decreases the level in increments, determined with
        the command [:SOURce<hw>]:POWer:STEP[:INCRement].

        """

        self.add_parameter('step_width_RF',
                        label='step_width_RF',
                        get_cmd='SOUR:POW:POW:STOP?',
                        set_cmd='SOUR:POW:POW:STOP{}',
                        vals=vals.Enum('DEC','USER') # RST: DEC
                                 )
        
        #Specifies the step width
        """
        Note: The command also sets "Variation Step" in the manual control, that means the
        user-defined step width for setting the level with the rotary knob or the [Up/Down]
        arrow keys.
        
        """

        self.add_parameter('step_width_RF_set',
                        label='step_width_RF_set',
                        get_cmd='SOUR:POW:STEP:INCR?',
                        set_cmd='SOUR:POW:STEP:INCR{}',
                        get_parser=float,
                        vals=vals.Numbers(0, 200) # Increment: 0.01; *RST: 1;  Default unit: dB
                                 )
        
        #Sets the level offset of a downstream instrument. The level at the RF output is not changed.

        self.add_parameter('offset_level_downstream_inst',
                        label='offset_level_downstream_inst',
                        get_cmd='SOUR:POW:LEV:IMM:OFFS?',
                        set_cmd='SOUR:POW:LEV:IMM:OFFS{}',
                        get_parser=float,
                        vals=vals.Numbers(-100, 100) # Increment: 0.01 , *RST: 0, Default unit: dB <- Always!

                                 )
        

        #Determines whether the current level is retained or if the stored level setting is adopted 
        #when an instrument configuration is loaded.

        self.add_parameter('which_level_conf',
                        label='which_level_conf',
                        get_cmd='SOUR:POW:LEV:IMM:RCL?',
                        set_cmd='SOUR:POW:LEV:IMM:RCL{}',
                        vals=vals.Enum('INCL','EXCL') #*RST: INCLude

                                 )

        #Sets the RF level applied to the DUT. 
        """
        To activate the RF output use command :OUTPut<hw>[:STATe] ("RF On"/"RF Off").
        The following applies POWer = RF output level + OFFSet, where:
        ● POWer is the values set with [:SOURce<hw>]:POWer[:LEVel][:
        IMMediate][:AMPLitude]
        ● RF output level is set with [:SOURce<hw>]:POWer:POWer
        ● OFFSet is set with [:SOURce<hw>]:POWer[:LEVel][:IMMediate]:OFFSet
        
        """


        self.add_parameter('RF_lvl_DUT',
                        label='RF_lvl_DUT',
                        get_cmd='SOUR:POW:LEV:IMM:AMPL?',
                        set_cmd='SOUR:POW:LEV:IMM:AMPL{}',
                        vals=vals.Enum('UP','DOWN') #*RST: -30  dBm

                                 )

        #Queries the current interruption-free range of the level

        self.add_parameter('lower_range',
                        label='lower_range',
                        get_cmd='SOUR:POW:RANG:LOW?',
                        set_cmd='SOUR:POW:RANG:LOW?{}',
                        vals=vals.Enum() # return float in dBm

                                 )


        self.add_parameter('upper_range',
                        label='upper_range',
                        get_cmd='SOUR:POW:RANG:UPP?',
                        set_cmd='SOUR:POW:RANG:UPP?{}',
                        vals=vals.Enum() # return float in dBm

                                 )


    #Ignores level range warnings.
        self.add_parameter('range_warn_ignore',
                        label='range_warn_ignore',
                        get_cmd='SOUR:POW:WIGN?',
                        set_cmd='SOUR:POW:WIGN?{}',
                        vals=vals.Enum('0','1','ON','OFF') # *RST: n.a. (factory preset: 0)

                                 )




        #-------------------------- End of SOURce Subsystem


        self.add_function('reset', call_cmd='*RST')
        self.add_function('run_self_tests', call_cmd='*TST?')

        self.connect_message()





    def on(self) -> None:
        self.status('on')

    def off(self) -> None:
        self.status('off')


class RohdeSchwarz_SGS100A(RohdeSchwarzSGS100A):
    pass