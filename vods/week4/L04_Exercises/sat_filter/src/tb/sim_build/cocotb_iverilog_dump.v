module cocotb_iverilog_dump();
initial begin
    $dumpfile("sim_build/sat_filter_wrapper.fst");
    $dumpvars(0, sat_filter_wrapper);
end
endmodule
