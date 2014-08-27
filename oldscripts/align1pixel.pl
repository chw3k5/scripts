#!/usr/bin/env perl

use PGPLOT;
use POSIX;
use IO::Socket::INET;
use Time::HiRes qw ( usleep );

$command = "setbias 0\n";

while(1)
{
    $socket = new IO::Socket::INET (PeerHost => 'thzbias.sese.asu.edu', PeerPort => '9001', Proto => 'tcp') or die "ERROR connecting to server : $!\n";
    $socket->send($command);
    usleep(300000);
    $socket->recv($socketdata,1024);
    #print $socketdata;

    my @lines=split('\n', $socketdata);
    foreach $line (@lines)
    {
	@data = split('=',$line);
	chomp(@data);
	if(fmod($i,4)==0)
	{
	    $volts=$data[1];
	}
	elsif(fmod($i,4)==1)
	{
	    $current=$data[1];
	}
	else {}
	$i++;
    }
    pgbegin(0,'/xs',1,1);
    pgscf(1);                # Set character font
    pgslw(6);                # Set line width
    pgsch(5);              # Set character height
    pgsvp(0.05, 0.9, 0.1, 0.95);
    pgswin(0,1,0,1);
    pgbox('BCST', 0.0, 0, 'BCST', 0.0, 0);
    pgsci(3);
    $rounded=sprintf("V = %.2f", $volts);
    pgtext(0.25,0.6,$rounded);
    $rounded=sprintf("I = %.1f", $current);
    pgtext(0.25,0.45,$rounded);
    pgend();

    $socket->close();
    usleep(200000);
}

