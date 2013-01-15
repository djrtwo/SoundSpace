fun void test()
{
    SinOsc s => dac;
    
    1000 => s.freq;
    // infinite time-loop   
    while( true )
    {
        10::ms => now;
    }
}


//spork ~ test() @=> Shred off;
for (0 => int i; i < 3; i++)
{
    spork ~ test() @=> Shred @ off;
    1::second => now;
    off.exit();
    1::second => now;
}
5::second => now;
