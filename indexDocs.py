import sys, os
from src.docs.document import Document

if __name__ == "__main__":

    if len(sys.argv) < 3:
        print('Usage: python %s <doc_dir> <output_dir>' % sys.argv[0])
        exit(1)

    doc_dir = sys.argv[1]
    output_dir = sys.argv[2]

    d = Document()
    d.transform_docs_to_biterm(doc_dir)
    d.export_to_txt(output_dir)
