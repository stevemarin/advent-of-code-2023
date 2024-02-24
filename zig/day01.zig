const std = @import("std");

pub fn main() !void {
    var buffer: [1024]u8 = undefined;
    var fba = std.heap.FixedBufferAllocator.init(&buffer);
    const allocator = fba.allocator();

    const memory = try allocator.alloc(u8, 1024);
    defer allocator.free(memory);

    @memset(memory, 0);
    @memset(memory[0..4], '0');
    @memset(memory[4..8], '1');

    std.debug.print("aaa: {s}", .{memory});
}
