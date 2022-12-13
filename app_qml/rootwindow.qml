import QtQuick
import QtQuick.Controls
import QtQuick.Dialogs

Rectangle {
  id: root
  width: 600
  height: 400
  //color: "#777777"
  visible: true

  Rectangle {
    id: main_area
    width: root.width - 24
    height: root.height - 24
    //color: "#bbbbbb"
    anchors.centerIn: root

    TextArea {
      id: text_box

      text: "Some sample text"
      anchors.top: main_area.top
      anchors.right: main_area.right
      anchors.bottom: cool_button.top
      anchors.left: main_area.left
      anchors.bottomMargin: 12
    }

    Button {
      id: cool_button
      text: "Click Me"
      anchors.bottom: main_area.bottom
      anchors.right: main_area.right

      onClicked: {
        text_box.text = Date()
      }
    }

    Button {
      id: pick_file_btn
      text: "Pick a file"
      anchors.right: cool_button.left
      anchors.top: cool_button.top
      anchors.rightMargin: 12

      onClicked: {
        fileDialog.visible = true
      }
    }

    FileDialog {
      id: fileDialog
      title: "Please choose a file"
      fileMode: FileDialog.OpenFile
      onAccepted: {
        console.log("File bytes: " + python_backend.pronk(selectedFile))
        visible = false
      }
      onRejected: {
        console.log("Canceled")
        visible = false
      }
    }
  }

}
