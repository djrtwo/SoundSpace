
fun void patch_test()
{
    Patch p;
    3 => int N;
    ["PulseOsc", "SqrOsc", "Gain"] @=> string types[];
    p.init(N, 0);
    for (0 => int i; i < N ; i++)
    {
        p.init_gen(i, types[i]);
        <<<p.gen_types[i]>>>;
    }

    p.set_attr(2, "gain", 0.2);
    p.set_attr(0, "freq", 1);
    p.set_attr(0, "gain", 100);
    p.set_attr(1, "freq", 500);
    p.set_attr(1, "sync", 2);

    for (0 => int i; i < 5; i++)
    {
        spork ~ p.run_patch();
        2::second => now;
        p.kill_patch();
        2::second => now;
    }
}

patch_test();