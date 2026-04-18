import cadquery as cq

model = cq.importers.importStep("aircraft_model_final.step")
if not model:
    print("Model failed to load")
else:
    print("Parts:", len(model.objects))
