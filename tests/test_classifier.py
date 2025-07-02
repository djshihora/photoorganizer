from PIL import Image
from photo_organizer import classifier

ALLOWED = {"selfie", "document", "screenshot", "nature", "other"}

def _patch_dummy_classifier(monkeypatch, label="person"):
    class DummyTensor:
        def unsqueeze(self, dim):
            return self

    class DummyLogits:
        def argmax(self, dim):
            class Res:
                def __init__(self, val):
                    self._val = val
                def item(self):
                    return self._val
            return Res(0)

    class DummyCtx:
        def __enter__(self):
            pass
        def __exit__(self, exc_type, exc, tb):
            pass

    class DummyTorch:
        def no_grad(self):
            return DummyCtx()

    class DummyWeights:
        DEFAULT = type("DW", (), {"meta": {"categories": [label]}})

    monkeypatch.setattr(classifier, "_classifier", lambda t: DummyLogits())
    monkeypatch.setattr(classifier, "_transform", lambda img: DummyTensor())
    monkeypatch.setattr(classifier, "transforms", object(), raising=False)
    monkeypatch.setattr(classifier, "torch", DummyTorch(), raising=False)
    monkeypatch.setattr(classifier, "MobileNet_V2_Weights", DummyWeights, raising=False)
    monkeypatch.setattr(classifier, "load_classifier", lambda: None)


def test_classify_image_green_is_nature(monkeypatch):
    monkeypatch.setattr(classifier, "_classifier", None)
    monkeypatch.setattr(classifier, "_transform", None)
    monkeypatch.setattr(classifier, "load_classifier", lambda: None)
    img = Image.new("RGB", (10, 10), (0, 255, 0))
    cat = classifier.classify_image(img)
    assert cat == "nature"
    assert cat in ALLOWED


def test_classify_image_stubbed_selfie(monkeypatch):
    _patch_dummy_classifier(monkeypatch, label="person")
    img = Image.new("RGB", (5, 5))
    cat = classifier.classify_image(img)
    assert cat == "selfie"
    assert cat in ALLOWED
