module cocotb_iverilog_dump();
initial begin
    $dumpfile("sim_build/mux.fst");
    $dumpvars(0, mux);
end
endmodule
