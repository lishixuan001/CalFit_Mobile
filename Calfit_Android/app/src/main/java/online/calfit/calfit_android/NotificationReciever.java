package online.calfit.calfit_android;

import android.app.Notification;
import android.app.NotificationChannel;
import android.app.NotificationManager;
import android.app.PendingIntent;
import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.media.RingtoneManager;
import android.net.Uri;
import android.os.Build;
import android.support.v4.app.NotificationCompat;
import android.support.v4.app.NotificationManagerCompat;


import static android.content.Context.NOTIFICATION_SERVICE;

/**
 * Created by lishixuan001 on 6/1/19.
 */

public class NotificationReciever extends BroadcastReceiver {

    String contentText;
    public final String CHANNEL_ID = "100";

    @Override
    public void onReceive(Context context, Intent intent) {
        String intentAction = intent.getAction();
        if (intentAction.equals("notify_morning")) {
            contentText = "Your goal for today is ready!";
        } else {
            contentText = "Remember to upload your data!";
        }



        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
            NotificationChannel notificationChannel = new NotificationChannel(CHANNEL_ID, "100", NotificationManager.IMPORTANCE_DEFAULT);
            notificationChannel.setDescription("Reminder");

            NotificationManager notificationManager = (NotificationManager) context.getSystemService(NOTIFICATION_SERVICE);
            assert notificationManager != null;
            notificationManager.createNotificationChannel(notificationChannel);

            Intent intent_repeat = new Intent(context, RepeatingActivity.class);
            intent_repeat.setFlags(Intent.FLAG_ACTIVITY_CLEAR_TOP);

            PendingIntent pendingIntent = PendingIntent.getActivity(context, 100, intent_repeat, PendingIntent.FLAG_UPDATE_CURRENT);

            Notification.Builder builder;
            builder = new Notification.Builder(context, CHANNEL_ID);
            builder.setSmallIcon(R.drawable.logo)
                    .setContentIntent(pendingIntent)
                    .setContentText(contentText)
                    .setContentTitle("Calfit Reminder")
                    .setAutoCancel(true);

            NotificationManagerCompat notificationManagerCompat = NotificationManagerCompat.from(context);
            notificationManagerCompat.notify(100, builder.build());

            notificationManager.notify(100, builder.build());

        } else {
            NotificationManager notificationManager = (NotificationManager) context.getSystemService(NOTIFICATION_SERVICE);

            Intent intent_repeat = new Intent(context, RepeatingActivity.class);
            intent_repeat.setFlags(Intent.FLAG_ACTIVITY_CLEAR_TOP);

            // if we want ring on notification then uncomment below line//
            Uri alarmSound = RingtoneManager.getDefaultUri(RingtoneManager.TYPE_NOTIFICATION);

            PendingIntent pendingIntent = PendingIntent.getActivity(context, 100, intent_repeat, PendingIntent.FLAG_UPDATE_CURRENT);

            NotificationCompat.Builder builder = new NotificationCompat.Builder(context, intentAction)
                    .setSmallIcon(R.drawable.logo)
                    .setContentIntent(pendingIntent)
                    .setContentText(contentText)
                    .setContentTitle("Calfit Reminder")
                    .setSound(alarmSound)
                    .setAutoCancel(true);
            notificationManager.notify(100, builder.build());
        }
    }
}
