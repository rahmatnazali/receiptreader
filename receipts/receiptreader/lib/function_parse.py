import json
import class_general


def parse_json_to_receipt(json_file_pointer):
    json_dict = parse_json_to_dict(json_file_pointer)
    return parse_dict_to_receipt(json_dict)


def parse_json_to_dict(json_file_pointer):
    return json.load(json_file_pointer)


def parse_dict_to_receipt(json_dict):
    json_full_text = json_parse_fulltext(json_dict)
    json_list_of_elements = json_parse_list_of_anotations(
        json_parse_annotation(json_dict)
    )

    list_of_elements = []
    for element in json_list_of_elements:
        list_of_elements.append(
            class_general.Element(
                phrase=element['description'],
                top_left=class_general.Vertex(element['boundingPoly']['vertices'][0]),
                top_right=class_general.Vertex(element['boundingPoly']['vertices'][1]),
                bottom_right=class_general.Vertex(element['boundingPoly']['vertices'][2]),
                bottom_left=class_general.Vertex(element['boundingPoly']['vertices'][3]),
            )
        )

    return class_general.OCR(json_full_text, list_of_elements)


def json_parse_fulltext(json_dict):
    return json_dict.get('fullTextAnnotation').get('text', None)


def json_parse_annotation(json_dict):
    return json_dict.get('textAnnotations', [])


def json_parse_list_of_anotations(json_list_text_annotation):
    return json_list_text_annotation[1:]
