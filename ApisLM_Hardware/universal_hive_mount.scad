/*
  ApisLM Universal Hive Mount
  Zero-Cost Hardware Component
  
  Parametric OpenSCAD design to hook a smartphone onto a standard 
  Langstroth hive bottom board for EntranceMonitor.tsx analysis.
*/

// --- Parameters ---
phone_thickness = 12;      // Thickness of phone with case (mm)
phone_width = 80;          // Width of the phone (mm)
hive_board_thickness = 20; // Standard Langstroth bottom board thickness (mm)
mount_width = 30;          // Width of the printable mount (mm)
wall_thickness = 4;        // Sturdiness of the walls (mm)
angle = 75;                // Viewing angle for the camera (degrees)

module hive_hook() {
    difference() {
        // Outer hook block
        cube([hive_board_thickness + (wall_thickness*2), mount_width, 40]);
        // Inner cutout for the hive board
        translate([wall_thickness, -1, wall_thickness])
            cube([hive_board_thickness, mount_width + 2, 40]);
    }
}

module phone_cradle() {
    // The cradle that holds the phone
    rotate([0, 0, angle])
    difference() {
        cube([phone_thickness + (wall_thickness*2), mount_width, 50]);
        translate([wall_thickness, -1, wall_thickness])
            cube([phone_thickness, mount_width + 2, 50]);
        // Camera/Sensor cutout
        translate([-1, mount_width/4, 20])
            cube([phone_thickness + (wall_thickness*2) + 2, mount_width/2, 35]);
    }
}

module universal_mount() {
    union() {
        hive_hook();
        // Attach cradle to the hook at the optimal entrance angle
        translate([hive_board_thickness + wall_thickness, 0, 15])
            phone_cradle();
    }
}

// Render the mount
universal_mount();
