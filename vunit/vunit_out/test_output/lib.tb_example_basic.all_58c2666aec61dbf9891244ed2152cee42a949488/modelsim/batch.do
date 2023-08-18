onerror {quit -code 1}
source "C:/Users/velic/OneDrive/Desktop/python/vunit/vunit_out/test_output/lib.tb_example_basic.all_58c2666aec61dbf9891244ed2152cee42a949488/modelsim/common.do"
set failed [vunit_load]
if {$failed} {quit -code 1}
set failed [vunit_run]
if {$failed} {quit -code 1}
quit -code 0
