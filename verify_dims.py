import cadquery as cq
model = cq.importers.importStep("aircraft_model_final.step")
shape = model.val() # Compound
bb = shape.BoundingBox()
print(f"Size: X={bb.xlen:.2f}, Y={bb.ylen:.2f}, Z={bb.zlen:.2f}")
