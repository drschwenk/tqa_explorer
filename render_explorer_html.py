import os
import json
import jinja2
import argparse

j2env = jinja2.Environment()

diagram_page_html = """
<!DOCTYPE html>
<html>
  <head>
    <style type="text/css">
       .container {
          }
    </style>
  </head>
  <body style=max-width: 100px>
    <div class="container">
      <h1>Lesson: {{lesson}}</h1>
      <ul>
        {% for topic in topics %}
        <p>
        </p>
        <p>{{topic}}</p>
        {% endfor %}
      </ul>
    </div>
    <script src="http://code.jquery.com/jquery-1.10.2.min.js"></script>
    <script src="http://netdna.bootstrapcdn.com/bootstrap/3.0.0/js/bootstrap.min.js"></script>
  </body>
</html>
"""

combined_explorer_page = """
<!DOCTYPE html>
<html>
  <head>
    <style type="text/css">
    #content, html, body {
        height: 100%;
        color: #9a9a9a;
        font-family: "Source Sans Pro", Arial, Helvetica, sans-serif;
        font-size: 14pt;
        font-weight: 400;
        line-height: 1.65;
        }
        #left {
        float: left;
        width: 45%;
        height: 100%;
        overflow: scroll;
    }
    #right {
        float: left;
        width: 45%;
        height: 100%;
        overflow: scroll;
    }
    #sidebar {
        height: 100%;
        background:#45A9CD;
        color: #b5deff;
        font-size: 14pt;
        float:left;
        width: 10%;
        overflow: scroll;
    }
    </style>
  </head>
  <body>
<div class="w3-sidebar w3-bar-block" id="sidebar">
     &nbsp;
       <h2 class="w3-bar-item">&nbsp; Topics</h2>
        <hr>
        {% for topic in topics if topic.0 %}
        &nbsp;<a href=#{{topic.0}} class="w3-bar-item w3-button">{{topic.0}}</a>
        <br></br>
        {% endfor %}
    </div>
    <div id="content">
      <div id="left">

          <h1>&nbsp;&nbsp;&nbsp; Lesson: {{lesson}}</h1>
          <ul>
            {% for topic in topics %}
            <p>
            </p>
            <h3 id={{topic.0}}>{{topic.0}}</h3>
            <p>{{topic.1}}</p>
            {% endfor %}
          </ul>

      </div>
      <div id="right">
        <h1 id=Text Questions>&nbsp;&nbsp;&nbsp; Text Questions</h1>
          <ul>
            {% for question in questions%}
            <h3>{{question[0]}}</h3>
                {% for q_part in question[1]%}
                    <p>{{q_part}}</p>
                {% endfor %}
            <hr>
            {% endfor %}
                <p>&nbsp;</p>
            </ul>
      </div>
    </div>
    <script src="http://code.jquery.com/jquery-1.10.2.min.js"></script>
    <script src="http://netdna.bootstrapcdn.com/bootstrap/3.0.0/js/bootstrap.min.js"></script>
  </body>
</html>
"""

combined_explorer_page_w_diagram = """
<!DOCTYPE html>
<html>
  <head>
    <style type="text/css">
    #content, html, body {
        height: 100%;
        color: #9a9a9a;
        font-family: "Source Sans Pro", Arial, Helvetica, sans-serif;
        font-size: 14pt;
        font-weight: 400;
        line-height: 1.65;
        }
        #left {
        float: left;
        width: 45%;
        height: 100%;
        overflow: scroll;
    }
    #right {
        float: left;
        width: 45%;
        height: 100%;
        overflow: scroll;
    }
    #sidebar {
        height: 100%;
        background:#45A9CD;
        color: #b5deff;
        font-size: 14pt;
        float:left;
        width: 10%;
        overflow: scroll;
    }
    </style>
  </head>
  <body>
  <div class="w3-sidebar w3-bar-block" id="sidebar">
     &nbsp;
       <h2 class="w3-bar-item">&nbsp; Topics</h2>
        <hr>
        {% for topic in topics if topic.0 %}
         &nbsp;<a href=#{{topic.0}} class="w3-bar-item w3-button">{{topic.0}}</a>
        <br></br>
        {% endfor %}
         &nbsp;<a href=#Supplemental Diagrams class="w3-bar-item w3-button">Supplemental Diagrams</a>
        <br></br>
        <h3 class="w3-bar-item">&nbsp; Questions</h3>
        <hr>
         &nbsp;<a href=#Text Questions class="w3-bar-item w3-button">Text Questions</a>
        <br></br>
         &nbsp;<a href=#Diagram Questions class="w3-bar-item w3-button">Diagram Questions</a>
    </div>
    <div id="content">
      <div id="left">
          <h1>&nbsp;&nbsp;&nbsp; Lesson: {{lesson}}</h1>
          <ul>
            {% for topic in topics %}
            <p>
            </p>
            <h3 id={{topic.0}}>{{topic.0}}</h3>
            <p>{{topic.1}}</p>
            {% endfor %}
          </ul>
          <h1 id=Supplemental Diagrams>&nbsp;&nbsp;&nbsp; Supplemental Diagram Descriptions</h1>
          <ul>
            {% for diagram in diagrams%}
            <p>
            </p>
            <p>{{diagram}}</p>
            {% endfor %}
          </ul>
      </div>
      <div id="right">
        <h1 id=Text Questions>&nbsp;&nbsp;&nbsp; Text Questions</h1>
          <ul>
            {% for question in questions%}
            <h3>{{question[0]}}</h3>
                {% for q_part in question[1]%}
                    <p>{{q_part}}</p>
                {% endfor %}
            <hr>
            {% endfor %}
                <p>&nbsp;</p>
            </ul>
          <h1 id=Diagram Questions>&nbsp;&nbsp;&nbsp; Diagram Questions</h1>
            <ul>
            {% for question in diagram_questions%}
            <h3>{{question[0]}}</h3>
                {% for q_part in question[1]%}
                    <p>{{q_part}}</p>
                {% endfor %}
            <hr>
            {% endfor %}
                <p>&nbsp;</p>
            </ul>
      </div>
    </div>
    <script src="http://code.jquery.com/jquery-1.10.2.min.js"></script>
    <script src="http://netdna.bootstrapcdn.com/bootstrap/3.0.0/js/bootstrap.min.js"></script>
  </body>
</html>
"""


def make_lesson_data(lesson_json, rel_html_out_path=None):
    nested_text = []
    for topic, content in sorted(lesson_json['topics'].items(), key=lambda kv: kv[1]['globalID']):
        nested_text.append((content['topicName'], content['content']['text']))
        if content['content']['figures']:
            for figure in content['content']['figures']:
                image_link = '<img src="' + '../../' + figure['imagePath'] + '" width=500px>'
                image_caption = figure['caption']
                nested_text.append(('', image_link))
                nested_text.append(('', image_caption))
    
    for topic, content in lesson_json['adjunctTopics'].items():
        if topic == 'Vocabulary':
            nested_text.append((topic, ''))            
            for k, v in content.items():
                nested_text.append(('', k + ':  ' + v))
        else:
            nested_text.append((topic, content['content']['text']))
            if content['content']['figures']:
                for figure in content['content']['figures']:
                    image_link = '<img src="' + '../../' + figure['imagePath'] + '" width=500px>'
                    image_caption = figure['caption']
                    nested_text.append(('', image_link))
                    nested_text.append(('', image_caption))
    return nested_text


def make_lesson_wdq_data(lesson_json, question_type='nonDiagramQuestions'):
    nested_text = []
    for question in sorted(lesson_json['questions'][question_type].values(), key=lambda x: x['globalID']):
        if question['questionType'] in ["Direct Answer"]:
            continue
        this_question = [None, []]
        this_question[0] = question['globalID']
        if question_type == 'diagramQuestions':
            image_link = '<img src="' + '../../' + question['imagePath'] + '" width=500px>'
            this_question[1].append(image_link)
        this_question[0] = question['beingAsked']['processedText']
        for ac in sorted(question['answerChoices'].values(), key=lambda x: x['idStructural']):
            if question['correctAnswer']['processedText'] in [ac['processedText'], ac['idStructural'].replace('.', '').replace(')', '')]:
                this_question[1].append('<font color="red"> ' + ' '.join([' ', ac['idStructural'], ac['processedText']]) + '</font>')
            else:
                this_question[1].append(' '.join([' ', ac['idStructural'], ac['processedText']]))
        nested_text.append(this_question)
    return nested_text


def make_lesson_diagram_description_data(lesson_json):
    nested_text = []
    for description in sorted(list(lesson_json['instructionalDiagrams'].values()), key=lambda x: x['imagePath']):
        image_link = '<img src="' + '../../' + description['imagePath'] + '" width=500px>'
        nested_text.append(image_link)
        nested_text.append(description['imageName'])
        being_asked = description['processedText']
        nested_text.append(being_asked)
        nested_text.append('')
    return nested_text


def make_page_html(lesson_data, page_html):
    return j2env.from_string(page_html).render(lesson=lesson_data[0], topics=lesson_data[1])


def make_explorer_html(lesson_data, question_data, page_html):
    return j2env.from_string(page_html).render(lesson=lesson_data[0], topics=lesson_data[1], questions=question_data)


def make_explorer_html_diagrams(lesson_data, question_data, page_html, diagram_description_data, diagram_question_data):
    return j2env.from_string(page_html).render(lesson=lesson_data[0], topics=lesson_data[1], questions=question_data,
                                               diagrams=diagram_description_data, diagram_questions=diagram_question_data)


def display_lesson_html(lesson_json, lesson, html_output_dir=None):
    lesson_data = (lesson, make_lesson_data(lesson_json, html_output_dir))
    question_data = make_lesson_wdq_data(lesson_json)
    diagram_description_data = make_lesson_diagram_description_data(lesson_json)
    if diagram_description_data:
        page_html = combined_explorer_page_w_diagram
        diagram_question_data = make_lesson_wdq_data(lesson_json, 'diagramQuestions')
        lesson_html = make_explorer_html_diagrams(lesson_data, question_data, page_html, diagram_description_data, diagram_question_data)
    else:
        page_html = combined_explorer_page
        lesson_html = make_explorer_html(lesson_data, question_data, page_html)
    return lesson_html


def make_lesson_html(flexbook, lesson, page_html):
    lesson_json = flexbook[lesson]
    lesson_data = (lesson, make_lesson_data(lesson_json))
    lesson_html = make_page_html(lesson_data, page_html)
    return lesson_html


def render_html_from_dataset(path_to_data_json):
    with open('subj_lookup.json', 'r') as f:
        subject_lookup = json.load(f)
    with open(path_to_data_json, 'r') as f:
        ck12_combined_dataset = json.load(f)
    out_path = '../dataset_explorer_pages'
    html_dir = os.path.join('dataset_explorer_pages', 'science')
    if not os.path.exists(html_dir):
        os.makedirs(html_dir)
    for lesson in ck12_combined_dataset:
        subject = subject_lookup[lesson['globalID']]
        if subject == 'skip':
            continue
        lesson_html = display_lesson_html(lesson, lesson['lessonName'], out_path)
        html_out_file = os.path.join(html_dir, subject + '/' + lesson['lessonName'].replace(' ', '_') + '_' + lesson['globalID'] + '.html')
        with open(html_out_file, 'w') as f:
            f.write(lesson_html.encode('ascii', 'ignore').decode('utf-8'))
            

def main():
    parser = argparse.ArgumentParser(description='Generates HTML pages from the dataset for review')
    parser.add_argument('dataset', help='path to complete dataset', type=str)
    args = parser.parse_args()
    data_path = args.dataset
    render_html_from_dataset(data_path)
   

if __name__ == "__main__":
    main()
