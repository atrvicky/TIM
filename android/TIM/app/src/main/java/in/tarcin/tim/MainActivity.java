package in.tarcin.tim;

import android.app.Activity;
import android.content.Context;
import android.content.Intent;
import android.os.Bundle;
import android.speech.RecognitionListener;
import android.speech.SpeechRecognizer;
import android.view.View;
import android.widget.ImageView;
import android.widget.ScrollView;
import android.widget.TextView;

import androidx.appcompat.app.AppCompatActivity;

import com.bumptech.glide.Glide;

import java.util.ArrayList;

public class MainActivity extends AppCompatActivity {

    private static SpeechRecognizer recognizer;
    RecognitionListener listener;
    ImageView gifView;
    private TextView status;
    private Context context;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        context = this;
        status = findViewById(R.id.status_output);
        gifView = findViewById(R.id.gif_view);

        Glide.with(context)
                .load(R.drawable.standby)
                .into(gifView);

        listener = new RecognitionListener() {
            CharSequence stat = "";

            @Override
            public void onReadyForSpeech(Bundle params) {

            }

            @Override
            public void onBeginningOfSpeech() {
                stat = context.getString(R.string.process_begin_recognition) + "\n";
                status.append(stat);
                Glide.with(context)
                        .load(R.drawable.listen)
                        .into(gifView);
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
                Glide.with(context)
                        .load(R.drawable.think)
                        .into(gifView);
            }

            @Override
            public void onError(int error) {
                stat = context.getString(R.string.process_error) + "\n";
                status.append(stat);
                status.append(error + "\n");
                Glide.with(context)
                        .load(R.drawable.standby)
                        .into(gifView);
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
                Glide.with(context)
                        .load(R.drawable.standby)
                        .into(gifView);
                ScrollView scrollView = ((Activity) context).findViewById(R.id.status_scrollView);
                scrollView.fullScroll(View.FOCUS_DOWN);
                analyzeAndAct(res.get(0));
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

    private void analyzeAndAct(String input) {
        if (input.equalsIgnoreCase("idiot")) {
            // do something
            status.append("thank you");
        } else if (input.equalsIgnoreCase("what is your name")) {
            // do something else
            status.append("tim");
        } else if (input.equalsIgnoreCase("hey tim")) {
            status.append("how can i help you");
            // do something else
        } else if (input.equalsIgnoreCase("d")) {
            // do something else
        } else if (input.equalsIgnoreCase("e")) {
            // do something else
        } else if (input.equalsIgnoreCase("f")) {
            // do something else
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
