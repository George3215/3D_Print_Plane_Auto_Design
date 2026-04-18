import cadquery as cq

print("Loading step file...")
model = cq.importers.importStep("aircraft_model_final.step")

print("Exporting Top View...")
cq.exporters.export(model, "blueprint_top.svg", opt={"projectionDir": (0, 0, 1), "showHidden": False})

print("Exporting Front View...")
cq.exporters.export(model, "blueprint_front.svg", opt={"projectionDir": (0, -1, 0), "showHidden": False})

print("Exporting Side View...")
cq.exporters.export(model, "blueprint_side.svg", opt={"projectionDir": (1, 0, 0), "showHidden": False})

print("Done generating blueprints.")
