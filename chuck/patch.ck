public class Patch
{
    UGen     patch_chain[];
    string   gen_types[];
    int      is_init[];
    int N;
    int id;
    Shred @ patch;
    int running;
    int is_chucked;
    
    // NEED TO MAKE FUNCTION THAT IS SPORKED AND LISTENS FOR UGEN ATTR UPDATES
    // /set_attr/patch_id/ugen_id ',sf' attr value
    
    fun void init(int size, int patch_id)
    {
        size => N;
        patch_id => id;
        UGen temp_chain[size] @=> patch_chain;
        string temp_types[size] @=> gen_types;
        int temp_inits[size] @=> is_init;
        
        0 => running;
        0 => is_chucked;
    }
    
    fun void init_gen(int index, string type)
    {
        // set type in gen_types
        type @=> gen_types[index];

        
        // create proper UGen
        // oscillators
        if (type == "Phasor")        Phasor   temp @=> patch_chain[index];
        else if (type == "SinOsc")   SinOsc   temp @=> patch_chain[index];
        else if (type == "PulseOsc") PulseOsc temp @=> patch_chain[index];
        else if (type == "SqrOsc")   SqrOsc   temp @=> patch_chain[index];
        else if (type == "TriOsc")   TriOsc   temp @=> patch_chain[index];
        else if (type == "SawOsc")   SawOsc   temp @=> patch_chain[index];
        // gain
        else if (type == "Gain")     Gain     temp @=> patch_chain[index];
        
        <<<"init " + type + ": ">>>;
        <<<patch_chain[index]>>>;
        
        1 => is_init[index];

        // if initialized, run patch
        1 => int initialized;
        for (0 => int i; i < N; i++)
        {
            if (is_init[i] == 0)
            {
                0 => initialized;
                break;
            }
        }
        
        if (initialized == 1)
            spork ~ run_patch();
        
    }
    
    fun void set_attr(int index, string attr, float val)
    {
        Utils.set_attr(attr, gen_types[index], patch_chain[index] $ UGen, val);
    }
    
    fun void chuck_patch()
    {
        for (0 => int i; i < N; i++)
        {
            if (i == N-1)
                patch_chain[i] => dac;
            else
                patch_chain[i] => patch_chain[i+1];
        }
        1 => is_chucked;
    }
    
    fun void unchuck_patch()
    {
        for (N-1 => int i; i >= 0; i--)
        {
            if (i == N-1)
                patch_chain[i] =< dac;
            else
                patch_chain[i] =< patch_chain[i+1];
        }
        0 => is_chucked;
    }
    
    // chucks patch if need be
    // runs the current patch
    fun void run_patch()
    {
        // patch each ugen into eachother
        if (is_chucked != 1)
        {
            chuck_patch();
        }
        
        1 => running;
        while (running == 1)
        {
            10::ms => now;
        }
        unchuck_patch();
    }
    
    fun void kill_patch()
    {
        0 => running;
    }
    
    //
    // functions to be sporked that listen for OSC events
    //
    fun void init_osc()
    {
        spork ~ osc_set_ugen();
        spork ~ osc_set_attr();
        // keep it running so children do no become abandoned
        while (true)
        { 10::ms => now;}
    }
    
    fun void osc_set_ugen()
    {
        "/set_ugen/" + id + ", i s" => string event_str;
        Utils.setup_listener(event_str) @=> OscEvent set_ugen_event;   
        
        while (true)
        {
            set_ugen_event => now;
            if (set_ugen_event.nextMsg() != 0)
            {
                set_ugen_event.getInt() => int index;
                set_ugen_event.getString() => string type;
                init_gen(index, type);
            }
            else
            {
                10::ms => now;
            }
        }
    }
    
    fun void osc_set_attr()
    {
        "/set_attr/" + id + ", i s f" => string event_str;   
        Utils.setup_listener(event_str) @=> OscEvent set_attr_event; 

        while (true)
        {
            set_attr_event => now;
            if (set_attr_event.nextMsg() != 0)
            {
                set_attr_event.getInt() => int index;
                set_attr_event.getString() => string attr;
                set_attr_event.getFloat() => float value;
/*                <<<"setting attr for id = " + id>>>;*/
                set_attr(index, attr, value);
            }
            else
            {
                10::ms => now;
            }
        }
    }
    
}

/*fun void test()
{
    Patch p;
    5 => int N;
    ["Phasor", "SinOsc", "PulseOsc", "SawOsc", "Gain"] @=> string types[];
    p.init(N);
    for (0 => int i; i < N ; i++)
    {
        p.init_gen(i, types[i]);
        <<<p.gen_types[i]>>>;
    }
    
    p.run_patch();
}

test();*/