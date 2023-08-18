onerror {quit -code 1}
source "C:/Users/velic/OneDrive/Desktop/python/vunit/vunit_out/test_output/lib.tb_example.Test_that_a_successful_test_case_passes2bdda5abfac164787ee41954d1c48bd036699331/modelsim/common.do"
set failed [vunit_load]
if {$failed} {quit -code 1}
set failed [vunit_run]
if {$failed} {quit -code 1}
quit -code 0
