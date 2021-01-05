#!/usr/bin/env perl
# -*- mode: cperl; indent-tabs-mode: nil; tab-width: 3; cperl-indent-level: 3; -*-
# Copyright (C) 2014, Apertium Project Management Committee <apertium-pmc@dlsi.ua.es>
# Licensed under the GNU GPL version 2 or later; see https://www.gnu.org/licenses/
use utf8;
use strict;
use warnings;
BEGIN {
	$| = 1;
	binmode(STDIN, ':encoding(UTF-8)');
	binmode(STDOUT, ':encoding(UTF-8)');
}
use open qw( :encoding(UTF-8) :std );

my $did = 1;
for (my $i=1 ; $i<1000 && $did ; $i++) {
   $did = 0;

   print STDERR "Round $i\n";

   my @syms = split("\n", `find lib/ -type l`);
   foreach my $s (@syms) {
      my $d = readlink($s);
      if (!-e "lib/$d" && -e "/opt/osx/lib/$d") {
         print STDERR "\tcopying real file '$d'\n";
         `rsync -avu '/opt/osx/lib/$d' 'lib/$d'`;
         if (-e "/opt/icudata/$d") {
            `rsync -avu '/opt/icudata/$d' 'lib/$d'`;
         }
         $did = 1;
      }
      if (!-e "lib/$d" && -e "/opt/osxcross/target/macports/pkgs/opt/local/lib/$d") {
         print STDERR "\tcopying real file '$d'\n";
         `rsync -avu '/opt/osxcross/target/macports/pkgs/opt/local/lib/$d' 'lib/$d'`;
         if (-e "/opt/icudata/$d") {
            `rsync -avu '/opt/icudata/$d' 'lib/$d'`;
         }
         $did = 1;
      }
   }

   my @files = split("\n", `find bin/ lib/ -type f`);
   foreach my $f (@files) {
      chomp($f);
      if (!$f) {
         next;
      }
      print STDERR "Handling '$f':\n";

      my @ldeps = split("\n", `x86_64-apple-darwin13-otool -L '$f' | grep /opt/osx/lib`);
      foreach my $d (@ldeps) {
         ($d) = ($d =~ m@/opt/osx/lib/(\S+)@);
         if ($f =~ m@\Q$d\E$@) {
            print STDERR "\tskipping self $d\n";
            next;
         }
         if (!-e "lib/$d" && -e "/opt/osx/lib/$d") {
            print STDERR "\tcopying l-dependency '$d'\n";
            `rsync -avu '/opt/osx/lib/$d' 'lib/$d'`;
            if (-e "/opt/icudata/$d") {
               `rsync -avu '/opt/icudata/$d' 'lib/$d'`;
            }
         }
         print STDERR "\tadjusting l-dependency '$d'\n";
         print STDERR `x86_64-apple-darwin13-install_name_tool -change '/opt/osx/lib/$d' '\@rpath/$d' '$f'`;
         $did = 1;
      }

      my @ndeps = split("\n", `x86_64-apple-darwin13-otool -L '$f' | egrep '^\\s+lib'`);
      foreach my $d (@ndeps) {
         ($d) = ($d =~ m@^\s+(\S+)@);
         if ($f =~ m@\Q$d\E$@) {
            print STDERR "\tskipping self $d\n";
            next;
         }
         if (-l "lib/$d" && "lib/".readlink("lib/$d") eq $f) {
            print STDERR "\tskipping sym-self $d\n";
            next;
         }
         if (!-e "lib/$d" && -e "/opt/osx/lib/$d") {
            print STDERR "\tcopying n-dependency '$d'\n";
            `rsync -avu '/opt/osx/lib/$d' 'lib/$d'`;
            if (-e "/opt/icudata/$d") {
               `rsync -avu '/opt/icudata/$d' 'lib/$d'`;
            }
         }
         print STDERR "\tadjusting n dependency '$d'\n";
         print STDERR `x86_64-apple-darwin13-install_name_tool -change '$d' '\@rpath/$d' '$f'`;
         $did = 1;
      }

      my @deps = split("\n", `x86_64-apple-darwin13-otool -L '$f' | egrep '/opt/local/lib'`);
      if (!@deps && !@ldeps) {
         next;
      }

      print STDERR "\tadding RPATH\n";
      `x86_64-apple-darwin13-install_name_tool -add_rpath \@executable_path/ '$f' 2>/dev/null`;
      `x86_64-apple-darwin13-install_name_tool -add_rpath \@executable_path/../lib '$f' 2>/dev/null`;
      `x86_64-apple-darwin13-install_name_tool -add_rpath \@loader_path/../lib '$f' 2>/dev/null`;

      foreach my $d (@deps) {
         ($d) = ($d =~ m@/opt/local/lib/(\S+)@);
         if ($f =~ m@\Q$d\E$@) {
            print STDERR "\tskipping self $d\n";
            next;
         }
         if (-l "lib/$d" && "lib/".readlink("lib/$d") eq $f) {
            print STDERR "\tskipping sym-self $d\n";
            next;
         }
         print STDERR "\tcopying dependency '$d'\n";
         `rsync -avu '/opt/osxcross/target/macports/pkgs/opt/local/lib/$d' 'lib/$d'`;
         if (-e "/opt/icudata/$d") {
            `rsync -avu '/opt/icudata/$d' 'lib/$d'`;
         }
         print STDERR "\tadjusting g-dependency '$d'\n";
         print STDERR `x86_64-apple-darwin13-install_name_tool -change '/opt/local/lib/$d' '\@rpath/$d' '$f'`;
         $did = 1;
      }
   }
}
