onerror {quit -code 1}
source "C:/Users/velic/OneDrive/Desktop/python/vunit/vunit_out/test_output/lib.tb_example.Test_that_a_test_case_that_takes_too_lof763c9dbbd826025101721b40758dfe8d596eff6/modelsim/common.do"
set failed [vunit_load]
if {$failed} {quit -code 1}
set failed [vunit_run]
if {$failed} {quit -code 1}
quit -code 0
