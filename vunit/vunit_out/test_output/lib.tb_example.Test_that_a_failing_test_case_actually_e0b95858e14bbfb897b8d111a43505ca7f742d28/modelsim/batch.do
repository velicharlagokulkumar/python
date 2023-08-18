onerror {quit -code 1}
source "C:/Users/velic/OneDrive/Desktop/python/vunit/vunit_out/test_output/lib.tb_example.Test_that_a_failing_test_case_actually_e0b95858e14bbfb897b8d111a43505ca7f742d28/modelsim/common.do"
set failed [vunit_load]
if {$failed} {quit -code 1}
set failed [vunit_run]
if {$failed} {quit -code 1}
quit -code 0
