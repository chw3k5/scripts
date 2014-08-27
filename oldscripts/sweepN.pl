#!/usr/bin/env perl

use PGPLOT;
use POSIX;
use IO::Socket::INET;
use Term::ReadKey;

# Note that the sweep command syntax for the Supercam hardware is:
# sweep <channel#> <starting pot pos> <ending pot pos> <# of points>
# The sweep command syntax for the prototype system is:
# sweep <channel#> <ending pot pos>

# this sweep returns exacty 501 points and takes exactly 48 sec to run
# with feedback 0 (off) it goes from 1-2.5 mV
#$sweepcommand = "sweep 0 63500 61500 500 \n";

# this sweep returns exacty 501 points and takes exactly 48 sec to run
# with feedback 1 (on) it goes from 1.2-2.5 mV
$sweepcommand = "sweep 0 60000 55000 500 \n";



my $key;
ReadMode 4;

do {
# connect to the server, send a command, write server's reply to a file
$socket = new IO::Socket::INET (PeerHost => 'thzbias.sese.asu.edu', PeerPort => '9001', Proto => 'tcp') or die "ERROR connecting to server : $!\n";
$socket->send($sweepcommand);
#sleep(240);
sleep(48);  # increase w/ number of points, or loop w/ recv() until you get all data
open(FILE, '>sweep.dat');
$socket->recv($data,417600);
# $socket->recv($data,102400);
print FILE $data;
$socket->close();
close(FILE);

@data=0;
$volts=0;
$current=0;
$power=0;
$pot=0;
$loop=0;
@sortedvolts=0;
@sortedcurrent=0;
@sortedpwr=0;
$i=0;

# Now let's look at the data and plot it
# First, let's decode the data from the server
open(FILE, "sweep.dat") || die "Cannot open input file.\n";
while(<FILE>){
    @data = split('=');
    chomp(@data);
    if(fmod($i,4)==0)
    {
        $volts[$loop]=$data[1];
    }
    elsif(fmod($i,4)==1)
    {
	$current[$loop]=$data[1];
    }
    elsif(fmod($i,4)==2)
    {
	$power[$loop]=$data[1];
    }
    elsif(fmod($i,4)==3)
    {
	$pot[$loop]=$data[1];
	$loop++;
    }
    $i++;
}
close(FILE);

$i=0;
# write a nice formatted sweep file
open(FILE, '>sweep.csv');
foreach(@volts)
{
    print FILE "$volts[$i] $current[$i] $power[$i] $pot[$i]\n";
    $i++;
}
close(FILE);

print "Found ", $loop, " points to plot.\n";
@sortedcurrent = sort {$a <=> $b} @current; 
@sortedvolts = sort  {$a <=> $b} @volts; 
@sortedpwr = sort {$a <=> $b} @power;

#scale total power to fit on current scale
$scalefactor = ($sortedcurrent[-1]/$sortedpwr[-1])*0.9 +0;
$i=0;
foreach $entry (@power)
{
    $power[$i]=1.0*(($entry*=$scalefactor)-0.0);
    $i++;
}

pgbegin(0,'/xs',1,1);
pgscf(1);                # Set character font
pgslw(6);                # Set line width
pgsch(2);              # Set character height

pgenv(($sortedvolts[1]-0.3),($sortedvolts[-1]+0.3),($sortedcurrent[1]-10),($sortedcurrent[-1]+10),0,0);
$title="Channel 1";
pglabel("Vbias (mV)","Ibias (uA)",$title);
# set color
pgsci(3);
# feed in the data
pgline($loop-1,*volts,*current);
pgsci(4);
pgline($loop-1,*volts,*power);
pgend();

} until (defined($key = ReadKey(-1)));

print"Got key: $key\n";
ReadMode 0;
