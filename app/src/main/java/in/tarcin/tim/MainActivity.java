package in.tarcin.tim;

import android.content.Context;
import android.content.Intent;
import android.os.Bundle;
import android.speech.RecognitionListener;
import android.speech.SpeechRecognizer;
import android.view.View;
import android.widget.TextView;

import androidx.appcompat.app.AppCompatActivity;

import java.util.ArrayList;

public class MainActivity extends AppCompatActivity {

    private static SpeechRecognizer recognizer;
    private TextView status;
    private Context context;
    private RecognitionListener listener;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        context = this;
        status = findViewById(R.id.status_output);

        listener = new RecognitionListener() {
            CharSequence stat = "";

            @Override
            public void onReadyForSpeech(Bundle params) {

            }

            @Override
            public void onBeginningOfSpeech() {
                stat = context.getString(R.string.process_begin_recognition) + "\n";
                status.append(stat);
            }

            @Override
            public void onRmsChanged(float rmsdB) {
//                status.append("rms: " + rmsdB + "\n");
            }

            @Override
            public void onBufferReceived(byte[] buffer) {

            }

            @Override
            public void onEndOfSpeech() {
                stat = context.getString(R.string.process_end_recognition) + "\n";
                status.append(stat);
            }

            @Override
            public void onError(int error) {
                stat = context.getString(R.string.process_error) + "\n";
                status.append(stat);
                status.append(error + "\n");
            }

            @Override
            public void onResults(Bundle results) {
                ArrayList<String> res = results.getStringArrayList(SpeechRecognizer.RESULTS_RECOGNITION);
                float[] confidence = results.getFloatArray(SpeechRecognizer.CONFIDENCE_SCORES);
                stat = context.getString(R.string.process_obtained_results) + "\n";
                status.append(stat);

                assert res != null;
                assert confidence != null;
                stat = "'" + res.get(0) + "' confidence: " + confidence[0] + "\n";
                status.append(stat);
            }

            @Override
            public void onPartialResults(Bundle partialResults) {

            }

            @Override
            public void onEvent(int eventType, Bundle params) {
                stat = context.getString(R.string.process_state_changed) + ": " + eventType + "\n";
                status.append(stat);
            }
        };

        if (!SpeechRecognizer.isRecognitionAvailable(context)) {
            CharSequence str = context.getString(R.string.process_no_recognition_found) + "\n";
            status.append(str);
        } else {
            recognizer = SpeechRecognizer.createSpeechRecognizer(context);
            recognizer.setRecognitionListener(listener);
        }
    }

    public void onClick(View v) {
        CharSequence statusVal = "";
        switch (v.getId()) {
            case R.id.begin_procedure:
                statusVal = context.getText(R.string.process_initiating) + "\n";
                Intent intent = new Intent();
                recognizer.startListening(intent);
                break;
            case R.id.terminate_procedure:
                statusVal = context.getText(R.string.process_terminating) + "\n";
                recognizer.destroy();
                break;
            default:
                break;
        }
        status.append(statusVal);
    }

}
