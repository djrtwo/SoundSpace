public class Utils
{
    static int osc_base_port;
    
    // For generic UGen
    // Casts and calls correct set_attr
    fun static void set_attr(string attr, string type, UGen ugen, float val)
    {
        // Oscillators
        // Casts into PulseOsc to be generic
        if (type == "Phasor" || type == "SinOsc" || type == "PulseOsc" ||
                type == "SqrOsc" || type == "TriOsc" || type == "SawOsc")
        {
            set_attr(attr, ugen $ PulseOsc, val);
        }
        else if (type == "Gain")
        {
            set_attr(attr, ugen $ Gain, val);
        }
        
    }
    
    // PulseOsc (generic for all oscillators)
    fun static void set_attr(string attr, PulseOsc s, float val)
    {
        if      (attr == "freq")  val => s.freq;
        else if (attr == "sfreq") val => s.sfreq;
        else if (attr == "phase") val => s.phase;
        else if (attr == "sync")  val $ int => s.sync;
        else if (attr == "width") val => s.width;
        else if (attr == "gain")  val => s.gain;
    }
    
    // Gain
    fun static void set_attr(string attr, Gain g, float val)
    {
        if      (attr == "gain")  val => g.gain;
    }
    
    fun static OscEvent setup_listener(string event_str)
    {
        OscRecv orec_temp;
        Utils.osc_base_port => orec_temp.port;
        orec_temp.listen();
        
        return orec_temp.event(event_str);
    }
}

// initialize static data
9000 => Utils.osc_base_port;

/*fun void test()
{
    SinOsc s => Gain g => dac;
    
    UGen patch_chain[];
    UGen patches[2] @=> patch_chain;
    
    Utils.set_attr("freq", "SinOsc", s $ UGen, 300);
    Utils.set_attr("gain", "Gain", g $ UGen, 0.3);
    while( true ) { 100::ms => now; }
}

test();*/