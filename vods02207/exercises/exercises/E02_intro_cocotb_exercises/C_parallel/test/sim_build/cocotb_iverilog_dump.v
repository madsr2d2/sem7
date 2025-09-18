module cocotb_iverilog_dump();
initial begin
    $dumpfile("sim_build/parallel.fst");
    $dumpvars(0, parallel);
end
endmodule
