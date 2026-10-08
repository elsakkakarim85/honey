/*
  =============================================================================
                           ApisLM Enterprise IoT Enclosure
                                 (Zero-Cost Hardware)
  =============================================================================
  
  Parametric OpenSCAD design for a weatherproof, solar-powered Edge Node.
  Hooks directly onto Langstroth, Lyson, or Apimaye bottom boards.
  Features:
  - ESP32-CAM internal housing
  - Si7021 Temp/Humidity sensor ventilation grill
  - 5V Solar Cell roof mount (adjustable angle)
  - Universal adjustable bottom-board hook
  - Weather-drip edges to prevent moisture ingress
*/

// --- Global Parameters ---
// Hive Compatibility (1 = Langstroth, 2 = Lyson Poly, 3 = Apimaye)
hive_type = 1; 

// Base Measurements
board_thickness = (hive_type == 1) ? 20 : (hive_type == 2) ? 25 : 35;
wall = 3.5;                  // Wall thickness for FDM printing strength
width = 65;                  // Enclosure width
height = 85;                 // Enclosure height
depth = 45;                  // Enclosure internal depth
tolerance = 0.4;             // Printer tolerance

// Solar Roof Angle
roof_angle = 35;             // Optimal angle for sun capture

module venting_grill() {
    // Airflow vents for temperature/humidity sensors
    for(i = [0 : 5 : 40]) {
        translate([-5, 10 + i, -10])
            rotate([45, 0, 0])
            cube([width + 10, 2.5, 20]);
    }
}

module pcb_standoffs() {
    // Standard 2.5mm screw posts for ESP32 and Sensors
    positions = [
        [wall + 5, wall + 5, 0],
        [width - wall - 5, wall + 5, 0],
        [wall + 5, height - wall - 5, 0],
        [width - wall - 5, height - wall - 5, 0]
    ];
    for(p = positions) {
        translate(p)
        difference() {
            cylinder(h = 6, r = 3.5, $fn = 30);
            cylinder(h = 7, r = 1.25, $fn = 30); // 2.5mm hole
        }
    }
}

module camera_lens_port() {
    // Weatherproof cone for the ESP32-CAM lens
    translate([width/2, height - 25, -2])
    difference() {
        cylinder(h = wall + 4, r1 = 12, r2 = 9, $fn = 50);
        translate([0,0,-1]) cylinder(h = wall + 6, r1 = 8, r2 = 6, $fn = 50);
    }
}

module main_enclosure() {
    difference() {
        // Main Body
        cube([width, height, depth]);
        
        // Inner Cavity
        translate([wall, wall, wall])
            cube([width - (wall*2), height - (wall*2), depth]);
            
        // Subtractive Vents
        translate([0, 10, depth - wall - 2]) venting_grill();
        
        // Bottom Cable Routing
        translate([width/2 - 5, -2, wall]) cube([10, wall + 4, 10]);
    }
    
    // Add PCB Mounting Standoffs
    translate([0, 0, wall]) pcb_standoffs();
    
    // Add Camera Port
    camera_lens_port();
}

module solar_roof() {
    // Slanted roof to mount 5V solar cell and shed rain
    translate([0, height, depth])
    rotate([-roof_angle, 0, 0])
    union() {
        // Roof panel
        cube([width, 60, wall]);
        // Drip edge overhang
        translate([-2, -2, -2]) cube([width + 4, 64, 4]);
    }
}

module universal_hook() {
    // Hooks onto the hive entrance/bottom board
    translate([0, -board_thickness - wall*2, 0])
    difference() {
        // Hook Block
        cube([width, board_thickness + wall*2, depth / 2]);
        // Slot for hive board
        translate([-1, wall, -1])
            cube([width + 2, board_thickness, depth / 2 + 2]);
    }
}

module enterprise_edge_node() {
    union() {
        main_enclosure();
        solar_roof();
        universal_hook();
    }
}

// Render the entire assembly
enterprise_edge_node();
