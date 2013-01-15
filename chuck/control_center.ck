// needs to set up to listen for /new_patch bundles that have size, 
// then /set_gen/patch_id/gen_id str(UGen type)

OscRecv orec_new;
Utils.osc_base_port => orec_new.port;
orec_new.listen();

// format == /new_patch id length
orec_new.event("/new_patch, i i") @=> OscEvent @ new_patch_event;

while (true)
{
    new_patch_event => now;
    if (new_patch_event.nextMsg() != 0)
    {
        int id;
        int size;
        new_patch_event.getInt() => id;
        new_patch_event.getInt() => size;
/*        <<<"new patch! id = " + id + ", size = " + size>>>;*/
        Patch p;
        p.init(size, id);
        spork ~ p.init_osc();
    }
    else
    {
        10::ms => now;
    }
}