[audio, fs] = wavread('file1.wav');
axis tight;
subplot(2,1,1)
axis tight;
spectrogram(audio,256,200,256,fs,'yaxis')
axis tight;

subplot(2,1,2)
wavEnergy=audio(:,1);
time=(1/fs)*length(wavEnergy);
t=linspace(0,time,length(wavEnergy));
axis tight;
plot(t,wavEnergy);
