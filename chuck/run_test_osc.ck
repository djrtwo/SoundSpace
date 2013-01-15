OscRecv orec_test1;
Utils.osc_base_port => orec_test1.port;
orec_test1.listen();

OscRecv orec_test2;
Utils.osc_base_port => orec_test2.port;
orec_test2.listen();


orec_test1.event("/test, i s") @=> OscEvent test1_event; 
orec_test2.event("/test, s") @=> OscEvent test2_event; 

while ( true )
{
    test1_event => now;
    test2_event => now;
    if (test1_event.nextMsg() != 0)
    {
        <<<test1_event.getInt()>>>;
        <<<test1_event.getString()>>>;
    }
    if (test2_event.nextMsg() != 0)
    {
        <<<test2_event.getString()>>>;
    }
    
}