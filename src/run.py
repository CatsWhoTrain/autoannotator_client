import glob
import cv2
from pathlib import Path

from autoannotator.utils.image_reader import ImageReader

from autoannotator.detection.faces import FaceDetEnsemble, SCRFD, YOLOv7

from autoannotator.utils.image_alignment import ImageAlignmentRegression

from autoannotator.feature_extraction.faces.models.model_adaface import FaceFeatureExtractorAdaface
from autoannotator.feature_extraction.faces.models.model_insightface import FaceFeatureExtractorInsightface
from autoannotator.feature_extraction.faces.models.ensemble import FaceFeatureExtractionEnsemle

from autoannotator.clustering.methods.dbscan import ClusteringDBSCAN


def run(img_dir):
    clusters_dir = Path(img_dir) / 'clusters'
    clusters_dir.mkdir(exist_ok=True)

    img_files = glob.glob(f'{img_dir}/*')

    reader = ImageReader()

    # face detection
    models = [SCRFD(), YOLOv7()]
    fd_ensemble = FaceDetEnsemble(models=models)

    # alignment
    regressor = ImageAlignmentRegression()

    # feature extractor
    models = [FaceFeatureExtractorAdaface(), FaceFeatureExtractorInsightface()]
    fr_ensemble = FaceFeatureExtractionEnsemle(models=models)
    descriptors = []

    faces_arr = []
    face_id = 0
    for photo_id, img_file in enumerate(img_files):
        assert Path(img_file).is_file()
        img = reader(img_file)

        h, w, _ = img.shape

        faces = fd_ensemble(img)

        for face in faces:
            aligned_img = regressor(img, face.landmarks)

            aligned_save_img = cv2.cvtColor(aligned_img, cv2.COLOR_RGB2BGR)
            cv2.imwrite(f'{clusters_dir}/{face_id}.jpg', aligned_save_img)

            descriptor = fr_ensemble(aligned_img)
            descriptors.append(descriptor)

            crop_path = f'clusters/{face_id}.jpg'

            faces_arr.append((face, face_id, photo_id, img_file, crop_path, (h, w)))
            face_id += 1

        print(faces_arr)
        break

    # clusterization
    dbscan = ClusteringDBSCAN(type="sklearn", eps=0.01, min_samples=2)

    labels = dbscan(descriptors)

    # results
    results = {
        'totalTime': 0,
        'frames': [],
        'clusters': [],
    }

    # set clusters
    from collections import defaultdict
    clusters = defaultdict(list)
    for face_meta, label in zip(faces_arr, labels):
        face, face_id, photo_id, img_file, crop_path, (h, w) = face_meta
        clusters[label].append({
            'face_id': face_id,
            'photo_id': photo_id,
            'image': crop_path,
        })

    for cluster_id, faces in clusters.items():
        results['clusters'].append({
            'cluster_id': cluster_id,
            'faces': faces,
        })

    # set frames
    from collections import defaultdict
    faces = defaultdict(list)
    meta = {}
    for face_meta, label in zip(faces_arr, labels):
        face, face_id, photo_id, img_file, crop_path, (h, w) = face_meta

        landmarks = np.array(face.landmarks)
        landmarks = landmarks[:, :2].tolist()

        meta[photo_id] = (img_file, (h, w))
        faces[photo_id].append({
            "face_id": face_id,
            "cluster_id": label,
            "x1": face.bbox[0],
            "y1": face.bbox[1],
            "x2": face.bbox[2],
            "y2": face.bbox[3],
            "points": landmarks
        })

    for img_id in faces.keys():
        img_file, shape = meta[img_id]
        results['frames'].append({
            "photo_id": img_id,
            "image": img_file,
            "width": shape[1],
            "height": shape[0],
            "faces": faces[img_id]
        })

    return results
