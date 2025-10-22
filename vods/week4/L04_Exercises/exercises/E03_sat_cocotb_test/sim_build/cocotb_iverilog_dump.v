module cocotb_iverilog_dump();
initial begin
    $dumpfile("/home/madsr2d2/sem7/vods/week4/L04_Exercises/exercises/E03_sat_cocotb_test/sim_build/sat_filter.fst");
    $dumpvars(0, sat_filter);
end
endmodule
