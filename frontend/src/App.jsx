import { useEffect, useRef, useState } from "react";

function Icon({ type, size = 22 }) {
  const common = {
    width: size,
    height: size,
    viewBox: "0 0 24 24",
    fill: "none",
    stroke: "currentColor",
    strokeWidth: 1.8,
    strokeLinecap: "round",
    strokeLinejoin: "round",
  };

  const icons = {
    home: (
      <svg {...common}>
        <path d="M3 10.5 12 3l9 7.5" />
        <path d="M5 9.5V21h14V9.5" />
        <path d="M9 21v-6h6v6" />
      </svg>
    ),

    camera: (
      <svg {...common}>
        <path d="M4 7h4l1.5-2h5L16 7h4v12H4z" />
        <circle cx="12" cy="13" r="3.5" />
      </svg>
    ),

    history: (
      <svg {...common}>
        <path d="M3 12a9 9 0 1 0 3-6.7" />
        <path d="M3 4v5h5" />
        <path d="M12 7v5l3 2" />
      </svg>
    ),

    tips: (
      <svg {...common}>
        <path d="M9 18h6" />
        <path d="M10 21h4" />
        <path d="M8.5 15.5C7 14.3 6 12.4 6 10a6 6 0 1 1 12 0c0 2.4-1 4.3-2.5 5.5-.8.6-1.2 1.3-1.3 2.5h-4.4c-.1-1.2-.5-1.9-1.3-2.5Z" />
      </svg>
    ),

    settings: (
      <svg {...common}>
        <circle cx="12" cy="12" r="3" />
        <path d="M19.4 15a1.7 1.7 0 0 0 .3 1.9l.1.1-1.8 1.8-.1-.1a1.7 1.7 0 0 0-1.9-.3 1.7 1.7 0 0 0-1 1.5V20h-2.5v-.1a1.7 1.7 0 0 0-1-1.5 1.7 1.7 0 0 0-1.9.3l-.1.1-1.8-1.8.1-.1A1.7 1.7 0 0 0 8 15a1.7 1.7 0 0 0-1.5-1H6v-2.5h.5A1.7 1.7 0 0 0 8 10a1.7 1.7 0 0 0-.3-1.9l-.1-.1 1.8-1.8.1.1a1.7 1.7 0 0 0 1.9.3 1.7 1.7 0 0 0 1-1.5V5h2.5v.1a1.7 1.7 0 0 0 1 1.5 1.7 1.7 0 0 0 1.9-.3l.1-.1 1.8 1.8-.1.1a1.7 1.7 0 0 0-.3 1.9 1.7 1.7 0 0 0 1.5 1h.1V14h-.1a1.7 1.7 0 0 0-1.5 1Z" />
      </svg>
    ),

    sparkles: (
      <svg {...common}>
        <path d="m12 3 1.3 4.7L18 9l-4.7 1.3L12 15l-1.3-4.7L6 9l4.7-1.3L12 3Z" />
        <path d="m19 15 .7 2.3L22 18l-2.3.7L19 21l-.7-2.3L16 18l2.3-.7L19 15Z" />
      </svg>
    ),

    target: (
      <svg {...common}>
        <circle cx="12" cy="12" r="8" />
        <circle cx="12" cy="12" r="3" />
        <path d="M12 2v3M12 19v3M2 12h3M19 12h3" />
      </svg>
    ),

    brain: (
      <svg {...common}>
        <path d="M9 4a3 3 0 0 0-3 3v.5A3.5 3.5 0 0 0 7 14a3 3 0 0 0 3 3h1V6a3 3 0 0 0-2-2Z" />
        <path d="M15 4a3 3 0 0 1 3 3v.5A3.5 3.5 0 0 1 17 14a3 3 0 0 1-3 3h-1V6a3 3 0 0 1 2-2Z" />
        <path d="M9 8h2M13 8h2M9 12h2M13 12h2" />
      </svg>
    ),

    lightning: (
      <svg {...common}>
        <path d="M13 2 4 14h6l-1 8 9-12h-6z" />
      </svg>
    ),

    arrow: (
      <svg {...common}>
        <path d="M5 12h14" />
        <path d="m13 6 6 6-6 6" />
      </svg>
    ),

    user: (
      <svg {...common}>
        <circle cx="12" cy="8" r="3.5" />
        <path d="M5 21a7 7 0 0 1 14 0" />
      </svg>
    ),

    heart: (
      <svg {...common}>
        <path d="M20.8 8.7c0 5.5-8.8 10.3-8.8 10.3S3.2 14.2 3.2 8.7A4.7 4.7 0 0 1 12 6a4.7 4.7 0 0 1 8.8 2.7Z" />
      </svg>
    ),

    shield: (
      <svg {...common}>
        <path d="M12 3 20 6v5c0 5-3.4 8.5-8 10-4.6-1.5-8-5-8-10V6z" />
        <path d="m9 12 2 2 4-4" />
      </svg>
    ),
  };

  return icons[type] || null;
}

function App() {
  const [backendStatus, setBackendStatus] = useState("Checking...");
  const [activePage, setActivePage] = useState("Home");
  const [cameraStarted, setCameraStarted] = useState(false);
  const [sessionTime, setSessionTime] = useState(30);
  const [sessionActive, setSessionActive] = useState(false);
  const [sessionResults, setSessionResults] = useState({
  totalFrames: 0,
  detectedFrames: 0,
  notDetectedFrames: 0,
  correctFrames: 0,
  incorrectFrames: 0,
  poseCounts: {},
  confidenceTotal: 0,
  feedbackCounts: {},
});

const [sessionSummary, setSessionSummary] = useState(null);
const sessionResultsRef = useRef(sessionResults);

useEffect(() => {
  sessionResultsRef.current = sessionResults;
}, [sessionResults]);

  const [detectedPose, setDetectedPose] = useState("No pose detected");
const [mlConfidence, setMlConfidence] = useState(0);
const [postureCorrect, setPostureCorrect] = useState(false);
const [postureFeedback, setPostureFeedback] = useState(
  "Start the camera to begin AI analysis."
);

  const videoRef = useRef(null);
  const streamRef = useRef(null);
  const canvasRef = useRef(null);
  const analysisInProgressRef = useRef(false);

  useEffect(() => {
    const checkBackend = async () => {
      try {
        const response = await fetch(
          "http://127.0.0.1:8000/health"
        );

        if (!response.ok) {
          throw new Error("Backend request failed");
        }

        const data = await response.json();

        if (data.status === "healthy") {
          setBackendStatus("Connected");
        } else {
          setBackendStatus("Offline");
        }
      } catch (error) {
        console.error("Backend connection error:", error);
        setBackendStatus("Offline");
      }
    };

    checkBackend();
  }, []);  
  
  useEffect(() => {
    if (!cameraStarted) {
      return;
    }

    const analysisInterval = setInterval(() => {
      analyzeFrame();
    }, 1000);

    return () => {
      clearInterval(analysisInterval);
    };
  }, [cameraStarted]);

  const startCamera = async () => {
  try {
    const stream = await navigator.mediaDevices.getUserMedia({
      video: true,
      audio: false,
    });

    streamRef.current = stream;
    videoRef.current.srcObject = stream;

    setCameraStarted(true);
    setSessionActive(true);
    setSessionTime(30);
    setSessionResults({
  totalFrames: 0,
  detectedFrames: 0,
  notDetectedFrames: 0,
  correctFrames: 0,
  incorrectFrames: 0,
  poseCounts: {},
  confidenceTotal: 0,
  feedbackCounts: {},
});

    setDetectedPose("Waiting for pose...");
    setMlConfidence(0);
    setPostureCorrect(false);
    setPostureFeedback(
      "Position yourself 4–5 feet from the camera."
    );
  } catch (error) {
    console.error("Camera access error:", error);
    alert(
      "Camera access was denied or the camera could not be opened."
    );
  }
};
  const createSessionSummary = (results) => {
  const poseEntries = Object.entries(results.poseCounts)
    .filter(([pose]) => pose !== "uncertain");

  let mostDetectedPose = "No clearly recognized pose";
  let highestPoseCount = 0;

  poseEntries.forEach(([pose, count]) => {
    if (count > highestPoseCount) {
      mostDetectedPose = pose;
      highestPoseCount = count;
    }
  });

  const recognizedFrames =
    results.detectedFrames -
    (results.poseCounts.uncertain || 0);

  const recognizedConfidenceTotal =
  results.confidenceTotal;

  const averageConfidence =
    recognizedFrames > 0
      ? recognizedConfidenceTotal / recognizedFrames
      : 0;

  const postureFrames =
    results.correctFrames + results.incorrectFrames;

  const postureScore =
    postureFrames > 0
      ? (results.correctFrames / postureFrames) * 100
      : 0;

  let mainFeedback = "No feedback recorded.";

  const feedbackEntries =
    Object.entries(results.feedbackCounts);

  if (feedbackEntries.length > 0) {
    feedbackEntries.sort((a, b) => b[1] - a[1]);
    mainFeedback = feedbackEntries[0][0];
  }

  return {
    ...results,
    duration: 30,
    mostDetectedPose,
    uncertainFrames: results.poseCounts.uncertain || 0,
    recognizedFrames,
    averageConfidence,
    postureScore,
    mainFeedback,
  };
};
  const stopCamera = () => {
    if (streamRef.current) {
      streamRef.current.getTracks().forEach((track) => {
        track.stop();
      });

      streamRef.current = null;
    }

    if (videoRef.current) {
      videoRef.current.srcObject = null;
    }

    setSessionActive(false);
    setCameraStarted(false);
  };

  const captureFrame = () => {
  if (!videoRef.current || !canvasRef.current) {
    return;
  }

  const video = videoRef.current;
  const canvas = canvasRef.current;

  if (video.videoWidth === 0 || video.videoHeight === 0) {
    return;
  }

  canvas.width = video.videoWidth;
  canvas.height = video.videoHeight;

  const context = canvas.getContext("2d");

  context.drawImage(
    video,
    0,
    0,
    canvas.width,
    canvas.height
  );

  console.log("Frame captured:", canvas.width, "x", canvas.height);
};
  useEffect(() => {
    if (!sessionActive) {
      return;
    }

    const timerInterval = setInterval(() => {
      setSessionTime((previousTime) => {
  if (previousTime <= 1) {
    clearInterval(timerInterval);

    setSessionActive(false);

    setSessionSummary(
  createSessionSummary(sessionResultsRef.current)
);

console.log(
  "FINAL SESSION SUMMARY:",
  createSessionSummary(sessionResultsRef.current)
);

    stopCamera();

    return 0;
  }

  return previousTime - 1;
});
    }, 1000);

    return () => {
      clearInterval(timerInterval);
    };
  }, [sessionActive]);

const analyzeFrame = async () => {
  if (!videoRef.current || !canvasRef.current) {
    return;
  }

  if (analysisInProgressRef.current) {
    return;
  }

  const video = videoRef.current;
  const canvas = canvasRef.current;

  if (video.videoWidth === 0 || video.videoHeight === 0) {
    return;
  }

  analysisInProgressRef.current = true;

  canvas.width = video.videoWidth;
  canvas.height = video.videoHeight;

  const context = canvas.getContext("2d");

  context.drawImage(
    video,
    0,
    0,
    canvas.width,
    canvas.height
  );

  canvas.toBlob(async (blob) => {
    if (!blob) {
      analysisInProgressRef.current = false;
      return;
    }

    const formData = new FormData();
    formData.append("file", blob, "frame.jpg");

    try {
      const response = await fetch(
        "http://127.0.0.1:8000/analyze-frame",
        {
          method: "POST",
          body: formData,
        }
      );

      if (!response.ok) {
        throw new Error("AI analysis request failed.");
      }

      const data = await response.json();

      if (data.status !== "success") {
        return;
      }

      setSessionResults((previous) => {
        const nextResults = {
          ...previous,
          totalFrames: previous.totalFrames + 1,
        };

        if (!data.pose) {
          nextResults.notDetectedFrames =
            previous.notDetectedFrames + 1;

          return nextResults;
        }

        nextResults.detectedFrames =
          previous.detectedFrames + 1;

        if (data.pose === "uncertain") {
          nextResults.poseCounts = {
            ...previous.poseCounts,
            uncertain:
              (previous.poseCounts.uncertain || 0) + 1,
          };

          return nextResults;
        }

        nextResults.poseCounts = {
          ...previous.poseCounts,
          [data.pose]:
            (previous.poseCounts[data.pose] || 0) + 1,
        };

        nextResults.confidenceTotal =
          previous.confidenceTotal +
          (data.confidence || 0);

        if (data.posture) {
          if (data.posture.correct) {
            nextResults.correctFrames =
              previous.correctFrames + 1;
          } else {
            nextResults.incorrectFrames =
              previous.incorrectFrames + 1;
          }

          if (
            data.posture.feedback &&
            data.posture.feedback.length > 0
          ) {
            const feedback = data.posture.feedback[0];

            nextResults.feedbackCounts = {
              ...previous.feedbackCounts,
              [feedback]:
                (previous.feedbackCounts[feedback] || 0) + 1,
            };
          }
        }

        return nextResults;
      });

      if (data.pose === "uncertain") {
        setDetectedPose("Uncertain Pose");
      } else if (data.pose) {
        setDetectedPose(
          data.pose.replaceAll("_", " ")
        );
      } else {
        setDetectedPose("No pose detected");
      }

      setMlConfidence(data.confidence || 0);

      if (data.posture) {
        setPostureCorrect(
          data.posture.correct || false
        );

        if (
          data.posture.feedback &&
          data.posture.feedback.length > 0
        ) {
          setPostureFeedback(
            data.posture.feedback.join(" ")
          );
        } else {
          setPostureFeedback("No feedback available.");
        }
      } else {
        setPostureCorrect(false);
        setPostureFeedback(
          "No posture analysis available."
        );
      }
    } catch (error) {
      console.error(
        "AI analysis error:",
        error
      );
    } finally {
      analysisInProgressRef.current = false;
    }
  }, "image/jpeg");
};

  const navigation = [
    { name: "Home", icon: "home" },
    { name: "Live Session", icon: "camera" },
    { name: "History", icon: "history" },
    { name: "Tips", icon: "tips" },
    { name: "Settings", icon: "settings" },
  ];

  return (
    <div className="app">
      <div className="background-glow glow-one"></div>
      <div className="background-glow glow-two"></div>
      <div className="background-glow glow-three"></div>

      <header className="topbar">
  <div className="brand">
    <div className="brand-logo">
      <div className="lotus">✦</div>
    </div>

    <div>
      <div className="brand-name">
        Yoga <span>Motion AI</span>
      </div>

      <div className="brand-subtitle">
        Better Posture&nbsp; • &nbsp;Healthier You
      </div>
    </div>
  </div>

  <div className="topbar-right">

    <div className="system-status">
      <span className="status-dot"></span>

      <span>
        {backendStatus === "Connected"
          ? "System Ready"
          : backendStatus}
      </span>
    </div>

    <div className="signature">
      <span className="signature-name">
        Chandan Kumar Sahu
      </span>

      <span className="signature-spark">✦</span>
    </div>

  </div>
</header>
      <div className="layout">

        {/* SIDEBAR */}
        <aside className="sidebar">
          <div className="sidebar-label">WORKSPACE</div>

          <nav>
            {navigation.map((item) => (
              <button
                key={item.name}
                className={`nav-item ${
                  activePage === item.name ? "active" : ""
                }`}
                onClick={() => setActivePage(item.name)}
              >
                <Icon type={item.icon} size={21} />
                <span>{item.name}</span>

                {activePage === item.name && (
                  <span className="active-arrow">›</span>
                )}
              </button>
            ))}
          </nav>

          <div className="sidebar-bottom">
            <div className="mini-card">
              <div className="mini-icon">
                <Icon type="sparkles" size={19} />
              </div>

              <div>
                <div className="mini-title">AI Powered</div>
                <div className="mini-text">
                  Smart posture analysis
                </div>
              </div>
            </div>

            <div className="side-decoration">
              <span>Good</span>
              <span>Posture</span>
              <span>Better</span>
              <span>Future</span>
            </div>
          </div>
        </aside>

        {/* MAIN CONTENT */}
        <main className="content">

          {/* HERO / WELCOME INTRODUCTION */}
<section className="hero">

  <div className="hero-art">
    <div className="moon"></div>

    <div className="mountain mountain-back"></div>
    <div className="mountain mountain-front"></div>

    <div className="water-line"></div>

    <div className="yoga-silhouette">
      <div className="yoga-head"></div>
      <div className="yoga-body"></div>
      <div className="yoga-arm left"></div>
      <div className="yoga-arm right"></div>
      <div className="yoga-leg standing"></div>
      <div className="yoga-leg raised"></div>
    </div>

    <div className="hero-stars star-one">✦</div>
    <div className="hero-stars star-two">✧</div>
    <div className="hero-stars star-three">•</div>
  </div>

  <div className="hero-content">

    <div className="ai-pill">
      <Icon type="sparkles" size={17} />
      AI POWERED
    </div>

    <h1>
      Your Yoga Journey
      <br />
      Just Got Smarter
    </h1>

    <p className="hero-description">
      Welcome to Yoga Motion AI — your intelligent companion
      <br />
      for a smarter and more mindful yoga practice.
      <br />
      Improve your posture with real-time AI guidance.
    </p>

    <div className="feature-row">

      <div className="hero-feature">
        <div className="feature-icon blue">
          <Icon type="target" size={23} />
        </div>

        <div>
          <strong>Real-time</strong>
          <span>Pose Detection</span>
        </div>
      </div>

      <div className="feature-divider"></div>

      <div className="hero-feature">
        <div className="feature-icon pink">
          <Icon type="brain" size={23} />
        </div>

        <div>
          <strong>AI Posture</strong>
          <span>Analysis</span>
        </div>
      </div>

      <div className="feature-divider"></div>

      <div className="hero-feature">
        <div className="feature-icon yellow">
          <Icon type="lightning" size={23} />
        </div>

        <div>
          <strong>Instant</strong>
          <span>Feedback</span>
        </div>
      </div>

    </div>

  </div>

</section>


{/* LIVE CAMERA SECTION */}
<section className="camera-section">

  <div className="camera-card">

    <div className="camera-card-header">

      <div className="camera-title">
        <div className="camera-title-icon">
          <Icon type="camera" size={23} />
        </div>

        <span>Live Camera</span>
      </div>

      <div className="camera-status">
        <span></span>
        {cameraStarted ? "Camera Active" : "Camera Not Started"}
      </div>

    </div>

    <div className="camera-preview">

      {!cameraStarted && (
        <div className="camera-placeholder">

          <div className="camera-circle">
            <Icon type="camera" size={31} />
          </div>

          <h3>
            Your camera preview
            <br />
            will appear here
          </h3>

          <p>
            Position yourself about 4–5 feet from the camera
            <br />
            so your full body is completely visible.
          </p>

        </div>
      )}

      <video
        ref={videoRef}
        className={`camera-video ${
          cameraStarted ? "camera-video-visible" : ""
        }`}
        autoPlay
        playsInline
        muted
      />

      <canvas
        ref={canvasRef}
        style={{ display: "none" }}
      />

      <button
        className={`camera-button ${
          cameraStarted ? "stop-camera-button" : ""
        }`}
        onClick={cameraStarted ? stopCamera : startCamera}
      >
        <Icon type="camera" size={20} />

        {cameraStarted ? "Stop Camera" : "Start Camera"}
      </button>

      

    </div>

  </div>

</section>

          {/* LOWER CONTENT */}
          <section className="lower-grid">

            {/* AI ANALYSIS */}
            <div className="analysis-card">

              <div className="section-heading">
                <div className="heading-icon purple">
                  <Icon type="sparkles" size={22} />
                </div>

                <div>
                  <h2>AI Analysis</h2>
                  <p>Real-time insights for better posture</p>
                </div>
              </div>

              <div className="stats-grid">

                <div className="stat-card purple-card">
                  <div className="stat-icon purple-bg">
                    <Icon type="user" size={19} />
                  </div>

                  <div className="stat-label">
                    Detected Pose
                  </div>

                  <div className="stat-value">
  {detectedPose}
</div>

<div className="stat-small">
  {cameraStarted
    ? `${(mlConfidence * 100).toFixed(1)}% ML confidence`
    : "Waiting for camera..."}
</div>
                </div>

                <div className="stat-card blue-card">
                  <div className="stat-icon blue-bg">
                    <Icon type="target" size={19} />
                  </div>

                  <div className="stat-label">
                    ML Confidence
                  </div>

                  <div className="stat-value">
  {cameraStarted || sessionSummary
    ? `${(mlConfidence * 100).toFixed(1)}%`
    : "--"}
</div>

<div className="stat-small">
  {cameraStarted || sessionSummary
    ? "AI model confidence"
    : "Waiting for camera..."}
</div>
                </div>

                <div className="stat-card green-card">
                  <div className="stat-icon green-bg">
                    <Icon type="heart" size={19} />
                  </div>

                  <div className="stat-label">
                    Posture Status
                  </div>

                  <div className="stat-value">
  {!cameraStarted && !sessionSummary
    ? "Not Started"
    : postureCorrect
      ? "Correct"
      : "Needs Correction"}
</div>

<div className="stat-small">
  {!cameraStarted && !sessionSummary
    ? "Waiting for camera..."
    : postureCorrect
      ? "Good posture"
      : "Follow the feedback below"}
</div>
                </div>

              </div>

              <div className="feedback">

                <div className="feedback-icon">
                  💡
                </div>

                <div className="feedback-content">
                  <strong>Posture Feedback</strong>

                  <span>
  {postureFeedback}
</span>
                </div>
                {sessionSummary && (
  <div className="session-report">
    <div className="session-report-header">
      <div>
        <span className="report-label">SESSION COMPLETE</span>
        <h2>30-Second Session Report</h2>
        <p>Your AI analysis results from this session.</p>
      </div>
    </div>

    <div className="report-grid">
      <div className="report-item">
        <span>Session Duration</span>
        <strong>{sessionSummary.duration} sec</strong>
      </div>

      <div className="report-item">
        <span>Most Detected Pose</span>
        <strong>
          {sessionSummary.mostDetectedPose.replaceAll("_", " ")}
        </strong>
      </div>

      <div className="report-item">
        <span>Average ML Confidence</span>
        <strong>
          {(sessionSummary.averageConfidence * 100).toFixed(1)}%
        </strong>
      </div>

      <div className="report-item">
        <span>Detected Frames</span>
        <strong>{sessionSummary.detectedFrames}</strong>
      </div>

      <div className="report-item">
        <span>Correct Posture Frames</span>
        <strong>{sessionSummary.correctFrames}</strong>
      </div>

      <div className="report-item">
        <span>Correction-Needed Frames</span>
        <strong>{sessionSummary.incorrectFrames}</strong>
      </div>

      <div className="report-item">
        <span>No-Pose Frames</span>
        <strong>{sessionSummary.notDetectedFrames}</strong>
      </div>

      <div className="report-item">
        <span>Posture Score</span>
        <strong>
          {sessionSummary.postureScore.toFixed(1)}%
        </strong>
      </div>
    </div>

    <div className="report-feedback">
      <span>💡 Main Feedback</span>
      <strong>{sessionSummary.mainFeedback}</strong>
    </div>

    <button
      className="new-session-button"
      onClick={() => {
        setSessionSummary(null);
        setSessionTime(30);
        setDetectedPose("No pose detected");
        setMlConfidence(0);
        setPostureCorrect(false);
        setPostureFeedback(
          "Start the camera to begin AI analysis."
        );
      }}
    >
      Start New Session
    </button>
  </div>
)}

                <Icon type="arrow" size={21} />

              </div>

            </div>

            {/* WHY YOGA MOTION AI */}
            <div className="why-card">

              <div className="why-title">
                <span>✦</span>
                Why Yoga Motion AI?
              </div>

              <div className="why-list">

                <div className="why-item">
                  <div className="why-icon purple-circle">
                    <Icon type="user" size={20} />
                  </div>

                  <div>
                    <strong>Improve Posture</strong>
                    <span>Stand taller, feel better</span>
                  </div>
                </div>

                <div className="why-item">
                  <div className="why-icon pink-circle">
                    <Icon type="heart" size={20} />
                  </div>

                  <div>
                    <strong>Build Better Habits</strong>
                    <span>Small steps, big changes</span>
                  </div>
                </div>

                <div className="why-item">
                  <div className="why-icon green-circle">
                    <Icon type="shield" size={20} />
                  </div>

                  <div>
                    <strong>Smart Corrections</strong>
                    <span>Real-time guidance</span>
                  </div>
                </div>

                <div className="why-item">
                  <div className="why-icon blue-circle">
                    <Icon type="brain" size={20} />
                  </div>

                  <div>
                    <strong>AI-Powered Analysis</strong>
                    <span>ML + MediaPipe technology</span>
                  </div>
                </div>

              </div>

            </div>

          </section>

          {/* FOOTER */}
          <footer className="footer">

            <div className="footer-line"></div>

            <span>Yoga Motion AI</span>

            <b>•</b>

            <span>MediaPipe + Machine Learning + FastAPI</span>

            <div className="footer-line"></div>

          </footer>

        </main>
      </div>

      <style>{`
        * {
          box-sizing: border-box;
        }

        body {
          margin: 0;
          background: #020817;
        }

        button {
          font-family: inherit;
        }

        .app {
          min-height: 100vh;
          color: #eef4ff;
          font-family:
            Inter,
            ui-sans-serif,
            system-ui,
            -apple-system,
            BlinkMacSystemFont,
            "Segoe UI",
            sans-serif;
          background:
            radial-gradient(
              circle at 78% 20%,
              rgba(80, 45, 180, 0.18),
              transparent 28%
            ),
            radial-gradient(
              circle at 20% 70%,
              rgba(0, 130, 255, 0.10),
              transparent 30%
            ),
            #020817;
          overflow-x: hidden;
          position: relative;
        }

        .background-glow {
          position: fixed;
          width: 380px;
          height: 380px;
          border-radius: 50%;
          filter: blur(110px);
          pointer-events: none;
          opacity: 0.13;
        }

        .glow-one {
          background: #7c3cff;
          top: 180px;
          right: 50px;
        }

        .glow-two {
          background: #00aaff;
          left: -180px;
          bottom: 100px;
        }

        .glow-three {
          background: #ec3cff;
          right: 30%;
          top: -200px;
        }

        /* TOP BAR */

        .topbar {
          height: 92px;
          display: flex;
          align-items: center;
          justify-content: space-between;
          padding: 0 34px;
          border-bottom: 1px solid rgba(83, 137, 255, 0.22);
          background: rgba(2, 8, 23, 0.84);
          backdrop-filter: blur(18px);
          position: relative;
          z-index: 10;
        }

        .brand {
          display: flex;
          align-items: center;
          gap: 14px;
        }

        .brand-logo {
          width: 52px;
          height: 52px;
          border-radius: 16px;
          display: grid;
          place-items: center;
          color: #8ecbff;
          border: 1px solid rgba(96, 165, 250, 0.35);
          background:
            linear-gradient(
              145deg,
              rgba(65, 90, 255, 0.30),
              rgba(182, 45, 255, 0.18)
            );
          box-shadow:
            0 0 24px rgba(75, 100, 255, 0.18);
        }

        .lotus {
          font-size: 31px;
          transform: rotate(45deg);
          color: #6dd5ff;
          text-shadow:
            0 0 12px rgba(70, 190, 255, 0.9),
            0 0 25px rgba(160, 70, 255, 0.5);
        }

        .brand-name {
          font-size: 22px;
          font-weight: 800;
          letter-spacing: -0.6px;
        }

        .brand-name span {
          color: #a855f7;
          text-shadow: 0 0 20px rgba(168, 85, 247, 0.4);
        }

        .brand-subtitle {
          color: #82a3d5;
          font-size: 11px;
          margin-top: 4px;
          letter-spacing: 0.3px;
        }

        .topbar-right {
          display: flex;
          align-items: center;
          gap: 28px;
        }

        .system-status {
          display: flex;
          align-items: center;
          gap: 9px;
          padding: 10px 17px;
          border-radius: 30px;
          border: 1px solid rgba(0, 220, 190, 0.35);
          background: rgba(0, 190, 170, 0.07);
          color: #b4fff0;
          font-size: 13px;
          font-weight: 600;
          box-shadow: 0 0 24px rgba(0, 220, 190, 0.07);
        }

        .status-dot {
          width: 9px;
          height: 9px;
          border-radius: 50%;
          background: #00e0a4;
          box-shadow: 0 0 12px #00e0a4;
        }

        .signature {
          position: relative;
          min-width: 190px;
          text-align: right;
          padding-right: 5px;
        }

        .signature-name {
          font-family: "Brush Script MT", "Segoe Script", cursive;
          font-size: 21px;
          color: #d8dfff;
          font-style: italic;
          text-shadow: 0 0 15px rgba(130, 130, 255, 0.25);
        }

        .signature-spark {
          color: #ff5fc7;
          font-size: 17px;
          margin-left: 6px;
        }

        /* LAYOUT */

        .layout {
          display: flex;
          min-height: calc(100vh - 92px);
        }

        .sidebar {
          width: 220px;
          flex-shrink: 0;
          border-right: 1px solid rgba(70, 120, 230, 0.18);
          padding: 28px 16px;
          background: rgba(1, 7, 21, 0.72);
          position: relative;
          z-index: 5;
        }

        .sidebar-label {
          color: #4d6c9c;
          font-size: 10px;
          font-weight: 700;
          letter-spacing: 1.8px;
          padding: 0 14px 14px;
        }

        .nav-item {
          width: 100%;
          display: flex;
          align-items: center;
          gap: 15px;
          border: 0;
          color: #91abd3;
          background: transparent;
          padding: 13px 14px;
          margin-bottom: 5px;
          border-radius: 12px;
          font-size: 14px;
          cursor: pointer;
          text-align: left;
          transition: all 0.25s ease;
        }

        .nav-item:hover {
          color: #eef4ff;
          background: rgba(72, 91, 220, 0.10);
          transform: translateX(3px);
        }

        .nav-item.active {
          color: white;
          background:
            linear-gradient(
              100deg,
              rgba(58, 82, 215, 0.48),
              rgba(116, 44, 225, 0.27)
            );
          border: 1px solid rgba(108, 118, 255, 0.38);
          box-shadow:
            0 8px 30px rgba(65, 75, 220, 0.12),
            inset 0 0 20px rgba(120, 90, 255, 0.06);
        }

        .nav-item.active svg {
          color: #9db8ff;
          filter: drop-shadow(0 0 7px rgba(100, 130, 255, 0.8));
        }

        .active-arrow {
          margin-left: auto;
          color: #b59cff;
          font-size: 22px;
        }

        .sidebar-bottom {
          position: absolute;
          left: 16px;
          right: 16px;
          bottom: 28px;
        }

        .mini-card {
          display: flex;
          align-items: center;
          gap: 10px;
          padding: 12px;
          border-radius: 13px;
          border: 1px solid rgba(110, 95, 255, 0.20);
          background: rgba(78, 56, 180, 0.08);
        }

        .mini-icon {
          color: #c78cff;
        }

        .mini-title {
          font-size: 12px;
          font-weight: 700;
          color: #d9c9ff;
        }

        .mini-text {
          font-size: 9px;
          color: #687da6;
          margin-top: 2px;
        }

        .side-decoration {
          padding: 25px 8px 0;
          font-family: "Brush Script MT", "Segoe Script", cursive;
          font-size: 20px;
          line-height: 0.88;
          transform: rotate(-8deg);
          color: #8c67ff;
          opacity: 0.65;
        }

        .side-decoration span {
          display: block;
        }

        .side-decoration span:nth-child(2) {
          color: #b969ff;
        }

        .side-decoration span:nth-child(3) {
          color: #5cafff;
        }

        .side-decoration span:nth-child(4) {
          color: #46c8ff;
        }

        /* CONTENT */

        .content {
          flex: 1;
          min-width: 0;
          padding: 32px 28px 22px;
        }

        /* HERO */

        .hero {
          position: relative;
          min-height: 475px;
          border: 1px solid rgba(75, 120, 255, 0.22);
          border-radius: 23px;
          overflow: hidden;
          background:
            linear-gradient(
              110deg,
              rgba(8, 17, 52, 0.96),
              rgba(4, 13, 36, 0.82)
            );
          box-shadow:
            0 25px 80px rgba(0, 0, 0, 0.25),
            inset 0 1px rgba(255, 255, 255, 0.03);
        }

        .hero-content {
          position: relative;
          z-index: 3;
          padding: 48px 0 35px 40px;
          width: 57%;
        }

        .ai-pill {
          display: inline-flex;
          align-items: center;
          gap: 8px;
          color: #a9c8ff;
          font-size: 11px;
          font-weight: 700;
          letter-spacing: 0.6px;
          padding: 9px 15px;
          border: 1px solid rgba(76, 133, 255, 0.40);
          border-radius: 25px;
          background: rgba(27, 76, 190, 0.12);
          box-shadow: 0 0 20px rgba(60, 100, 255, 0.07);
        }

        .ai-pill svg {
          color: #c084fc;
        }

        .hero h1 {
  margin: 22px 0 18px;
  font-size: clamp(39px, 4vw, 57px);
  line-height: 0.98;
  letter-spacing: -2.5px;
  font-weight: 850;

  background:
    linear-gradient(
      90deg,
      #9b5cff,
      #4c9cff,
      #56d7ff
    );

  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;

  filter: drop-shadow(
    0 0 18px rgba(110, 75, 255, 0.24)
  );
}

.hero h1 span {
  background: none;
  color: inherit;
  filter: none;
}

        .hero-description {
          color: #91afd9;
          font-size: 14px;
          line-height: 1.65;
          margin: 0;
        }

        .feature-row {
          display: flex;
          align-items: center;
          margin-top: 27px;
          gap: 15px;
        }

        .hero-feature {
          display: flex;
          align-items: center;
          gap: 9px;
        }

        .hero-feature strong,
        .hero-feature span {
          display: block;
        }

        .hero-feature strong {
          font-size: 11px;
          color: #dbe8ff;
          font-weight: 700;
        }

        .hero-feature span {
          font-size: 10px;
          color: #7191c1;
          margin-top: 2px;
        }

        .feature-icon {
          width: 38px;
          height: 38px;
          border-radius: 11px;
          display: grid;
          place-items: center;
        }

        .feature-icon.blue {
          color: #72c5ff;
          background: rgba(46, 143, 255, 0.11);
        }

        .feature-icon.pink {
          color: #ee72ff;
          background: rgba(221, 55, 255, 0.11);
        }

        .feature-icon.yellow {
          color: #ffd55b;
          background: rgba(255, 193, 58, 0.11);
        }

        .feature-divider {
          width: 1px;
          height: 32px;
          background: rgba(104, 132, 190, 0.22);
        }

        .gradient-button {
          display: flex;
          align-items: center;
          gap: 11px;
          border: 0;
          margin-top: 29px;
          padding: 14px 20px;
          border-radius: 13px;
          color: white;
          font-size: 14px;
          font-weight: 700;
          cursor: pointer;
          background:
            linear-gradient(
              100deg,
              #a53cff,
              #655cff,
              #19bff5
            );
          box-shadow:
            0 12px 32px rgba(99, 67, 255, 0.32),
            inset 0 1px rgba(255, 255, 255, 0.28);
          transition: 0.25s ease;
        }

        .gradient-button:hover {
          transform: translateY(-3px);
          box-shadow:
            0 18px 38px rgba(99, 67, 255, 0.42);
        }

        .gradient-button svg:last-child {
          margin-left: 4px;
        }

        /* HERO ART */

        .hero-art {
          position: absolute;
          inset: 0;
          overflow: hidden;
          opacity: 0.95;
        }

        .hero-art::after {
          content: "";
          position: absolute;
          inset: 0;
          background:
            linear-gradient(
              90deg,
              rgba(3, 11, 31, 0.92) 0%,
              rgba(3, 11, 31, 0.68) 44%,
              rgba(3, 11, 31, 0.10) 75%
            );
        }

        .moon {
          position: absolute;
          width: 155px;
          height: 155px;
          border-radius: 50%;
          right: 32%;
          top: 73px;
          background:
            radial-gradient(
              circle at 40% 38%,
              #ffb6d8,
              #ff6eb7 42%,
              #8d4ce5 75%
            );
          box-shadow:
            0 0 60px rgba(255, 91, 190, 0.38);
        }

        .mountain {
          position: absolute;
          bottom: 0;
          width: 70%;
          height: 50%;
          clip-path: polygon(
            0 100%,
            18% 54%,
            31% 78%,
            46% 20%,
            59% 62%,
            73% 39%,
            100% 100%
          );
        }

        .mountain-back {
          right: -8%;
          background: #182359;
          opacity: 0.72;
        }

        .mountain-front {
          right: -2%;
          width: 65%;
          height: 42%;
          background: #09143a;
        }

        .water-line {
          position: absolute;
          right: 17%;
          bottom: 17%;
          width: 41%;
          height: 1px;
          background: linear-gradient(
            90deg,
            transparent,
            rgba(97, 181, 255, 0.65),
            transparent
          );
          box-shadow:
            0 -12px 0 rgba(90, 164, 255, 0.12),
            0 12px 0 rgba(90, 164, 255, 0.09);
        }

        .yoga-silhouette {
          position: absolute;
          right: 28%;
          bottom: 15%;
          width: 95px;
          height: 265px;
          z-index: 2;
          filter: drop-shadow(0 0 13px rgba(12, 15, 55, 0.9));
        }

        .yoga-head {
          position: absolute;
          width: 31px;
          height: 31px;
          border-radius: 50%;
          background: #090d27;
          left: 34px;
          top: 0;
        }

        .yoga-body {
          position: absolute;
          width: 37px;
          height: 110px;
          border-radius: 45% 45% 35% 35%;
          background: #090d27;
          left: 28px;
          top: 29px;
          transform: rotate(3deg);
        }

        .yoga-arm {
          position: absolute;
          height: 105px;
          width: 13px;
          background: #090d27;
          border-radius: 20px;
          top: 27px;
        }

        .yoga-arm.left {
          left: 24px;
          transform: rotate(34deg);
        }

        .yoga-arm.right {
          left: 60px;
          transform: rotate(-34deg);
        }

        .yoga-leg {
          position: absolute;
          height: 138px;
          width: 15px;
          background: #090d27;
          border-radius: 20px;
          top: 116px;
        }

        .yoga-leg.standing {
          left: 39px;
          transform: rotate(3deg);
        }

        .yoga-leg.raised {
          left: 57px;
          height: 104px;
          transform-origin: top;
          transform: rotate(-62deg);
        }

        .hero-stars {
          position: absolute;
          color: #9cc9ff;
          z-index: 2;
          opacity: 0.65;
        }

        .star-one {
          right: 40%;
          top: 70px;
          color: #ffd7ff;
        }

        .star-two {
          right: 14%;
          top: 90px;
          color: #7dd3fc;
        }

        .star-three {
          right: 22%;
          top: 42%;
          color: #c084fc;
        }

        /* CAMERA CARD */

        /* LIVE CAMERA SECTION */

.camera-section {
  width: 100%;
  margin-top: 24px;
}

.camera-card {
  position: relative;
  width: 100%;
  min-width: 0;
  min-height: 700px;

  padding: 20px;

  border-radius: 22px;

  border: 1px solid rgba(79, 202, 255, 0.65);

  background:
    linear-gradient(
      145deg,
      rgba(7, 29, 69, 0.84),
      rgba(16, 10, 46, 0.76)
    );

  box-shadow:
    0 0 32px rgba(46, 164, 255, 0.11),
    0 0 35px rgba(187, 61, 255, 0.08),
    inset 0 0 30px rgba(54, 92, 255, 0.05);
}

        .camera-card::before {
          content: "";
          position: absolute;
          inset: -1px;
          border-radius: 20px;
          padding: 1px;
          background: linear-gradient(
            130deg,
            #08c8ff,
            transparent 45%,
            #d03cff
          );
          -webkit-mask:
            linear-gradient(#fff 0 0) content-box,
            linear-gradient(#fff 0 0);
          -webkit-mask-composite: xor;
          mask-composite: exclude;
          pointer-events: none;
        }

        .camera-card-header {
          display: flex;
          justify-content: space-between;
          align-items: center;
          padding: 2px 4px 14px;
        }

        .camera-title {
          display: flex;
          align-items: center;
          gap: 11px;
          font-size: 17px;
          font-weight: 750;
        }

        .camera-title-icon {
          color: #4dd7ff;
        }

        .camera-status {
          font-size: 9px;
          color: #b0c2e2;
          padding: 7px 10px;
          border-radius: 20px;
          background: rgba(90, 110, 170, 0.12);
        }

        .camera-status span {
          display: inline-block;
          width: 7px;
          height: 7px;
          border-radius: 50%;
          background: #879ce7;
          margin-right: 6px;
        }

        .camera-preview {
  position: relative;

  width: 100%;
  height: 620px;

  border: 1px solid rgba(66, 135, 230, 0.45);

  border-radius: 16px;

  background:
    radial-gradient(
      circle at 50% 40%,
      rgba(28, 53, 105, 0.22),
      transparent 45%
    ),
    rgba(1, 10, 28, 0.75);

  display: flex;
  flex-direction: column;

  align-items: center;
  justify-content: space-between;

  padding: 12px;

  overflow: hidden;
}.camera-video {
  display: none;

  width: 100%;
  height: 100%;

  object-fit: contain;

  border-radius: 12px;

  background: #010817;
}

.camera-video-visible {
  display: block;
}

.camera-video-visible {
  display: block;
}

.camera-preview:has(.camera-video-visible) {
  padding: 8px;
}

.camera-preview:has(.camera-video-visible) .camera-button {
  position: absolute;
  bottom: 18px;
  left: 10%;
  width: 80%;
  z-index: 10;
}

.stop-camera-button {
  background: linear-gradient(
    90deg,
    #e83e8c,
    #a855f7,
    #6366f1
  );
}

        .camera-placeholder {
          text-align: center;
        }

        .camera-circle {
          width: 65px;
          height: 65px;
          border-radius: 50%;
          display: grid;
          place-items: center;
          margin: 0 auto 17px;
          color: #8eb9ff;
          border: 2px solid rgba(111, 159, 255, 0.72);
          box-shadow:
            0 0 22px rgba(77, 128, 255, 0.12),
            inset 0 0 20px rgba(77, 128, 255, 0.08);
        }

        .camera-placeholder h3 {
          font-size: 14px;
          line-height: 1.45;
          margin: 0;
          color: #e4ecff;
        }

        .camera-placeholder p {
          font-size: 11px;
          line-height: 1.5;
          color: #7996c5;
          margin: 9px 0 0;
        }

        .camera-button {
          width: 80%;
          height: 43px;
          border: 0;
          border-radius: 25px;
          color: white;
          background:
            linear-gradient(
              90deg,
              #5b43ef,
              #8c3eff,
              #10bce8
            );
          font-size: 13px;
          font-weight: 700;
          cursor: pointer;
          box-shadow:
            0 8px 25px rgba(91, 67, 239, 0.25);
          transition: 0.25s;
        }

        .camera-button:hover {
          transform: translateY(-2px);
          box-shadow:
            0 12px 32px rgba(91, 67, 239, 0.40);
        }

        /* LOWER GRID */

        .lower-grid {
          display: grid;
          grid-template-columns: minmax(0, 2fr) minmax(280px, 1fr);
          gap: 22px;
          margin-top: 22px;
        }

        .analysis-card,
        .why-card {
          border: 1px solid rgba(75, 125, 235, 0.24);
          border-radius: 18px;
          background:
            linear-gradient(
              145deg,
              rgba(7, 19, 47, 0.86),
              rgba(4, 13, 32, 0.92)
            );
          box-shadow:
            0 20px 55px rgba(0, 0, 0, 0.16),
            inset 0 1px rgba(255, 255, 255, 0.02);
        }

        .analysis-card {
          padding: 23px;
        }

        .section-heading {
          display: flex;
          align-items: center;
          gap: 11px;
        }

        .heading-icon {
          width: 37px;
          height: 37px;
          border-radius: 11px;
          display: grid;
          place-items: center;
        }

        .heading-icon.purple {
          color: #d69aff;
          background: rgba(171, 72, 255, 0.11);
        }

        .section-heading h2 {
          font-size: 18px;
          margin: 0;
        }

        .section-heading p {
          margin: 3px 0 0;
          color: #6884b1;
          font-size: 10px;
        }

        .stats-grid {
          display: grid;
          grid-template-columns: repeat(3, 1fr);
          gap: 13px;
          margin-top: 19px;
        }

        .stat-card {
          min-height: 140px;
          border-radius: 13px;
          padding: 14px;
          position: relative;
          overflow: hidden;
        }

        .stat-card::after {
          content: "";
          position: absolute;
          width: 90px;
          height: 90px;
          border-radius: 50%;
          right: -35px;
          bottom: -40px;
          filter: blur(18px);
          opacity: 0.14;
        }

        .purple-card {
          border: 1px solid rgba(180, 72, 255, 0.45);
          background: rgba(84, 32, 139, 0.12);
        }

        .blue-card {
          border: 1px solid rgba(50, 137, 255, 0.45);
          background: rgba(21, 66, 143, 0.12);
        }

        .green-card {
          border: 1px solid rgba(0, 220, 181, 0.42);
          background: rgba(0, 116, 101, 0.10);
        }

        .stat-icon {
          width: 29px;
          height: 29px;
          border-radius: 50%;
          display: grid;
          place-items: center;
          margin-bottom: 12px;
        }

        .purple-bg {
          color: #df9cff;
          background: rgba(164, 72, 255, 0.19);
        }

        .blue-bg {
          color: #7bc4ff;
          background: rgba(38, 123, 255, 0.18);
        }

        .green-bg {
          color: #6effd8;
          background: rgba(0, 210, 175, 0.17);
        }

        .stat-label {
          color: #a5b8d9;
          font-size: 11px;
          font-weight: 600;
        }

        .stat-value {
          color: #f1f5ff;
          font-size: 17px;
          font-weight: 750;
          margin-top: 5px;
        }

        .stat-small {
          color: #536d9b;
          font-size: 9px;
          margin-top: 5px;
        }

        .feedback {
          margin-top: 13px;
          display: flex;
          align-items: center;
          gap: 13px;
          padding: 13px 15px;
          border: 1px solid rgba(55, 157, 255, 0.35);
          border-radius: 12px;
          background: rgba(17, 74, 140, 0.10);
          color: #a8c5ec;
        }

        .feedback-icon {
          width: 35px;
          height: 35px;
          border-radius: 50%;
          display: grid;
          place-items: center;
          background: rgba(255, 199, 61, 0.14);
          font-size: 18px;
        }

        .feedback-content {
          flex: 1;
        }

        .feedback-content strong,
        .feedback-content span {
          display: block;
        }

        .feedback-content strong {
          font-size: 11px;
          color: #dbe9ff;
        }

        .feedback-content span {
          font-size: 9px;
          color: #6988b7;
          margin-top: 4px;
        }

        /* WHY CARD */

        .why-card {
          padding: 23px;
        }

        .why-title {
          font-size: 17px;
          font-weight: 750;
          display: flex;
          align-items: center;
          gap: 10px;
        }

        .why-title span {
          color: #6dc7ff;
          font-size: 23px;
        }

        .why-list {
          margin-top: 18px;
        }

        .why-item {
          display: flex;
          align-items: center;
          gap: 12px;
          margin-bottom: 16px;
        }

        .why-icon {
          width: 38px;
          height: 38px;
          border-radius: 50%;
          display: grid;
          place-items: center;
          flex-shrink: 0;
        }

        .purple-circle {
          color: #e09bff;
          background: rgba(158, 62, 255, 0.18);
        }

        .pink-circle {
          color: #ff80b8;
          background: rgba(255, 61, 132, 0.16);
        }

        .green-circle {
          color: #65f3c2;
          background: rgba(0, 209, 153, 0.15);
        }

        .blue-circle {
          color: #72c6ff;
          background: rgba(48, 139, 255, 0.16);
        }

        .why-item strong,
        .why-item span {
          display: block;
        }

        .why-item strong {
          color: #dce7fb;
          font-size: 11px;
        }

        .why-item span {
          color: #6685b4;
          font-size: 9px;
          margin-top: 4px;
        }

        /* FOOTER */

        .footer {
          display: flex;
          justify-content: center;
          align-items: center;
          gap: 14px;
          color: #55729f;
          font-size: 9px;
          padding: 22px 0 2px;
        }

        .footer b {
          color: #8161e8;
        }

        .footer-line {
          height: 1px;
          width: 80px;
          background: linear-gradient(
            90deg,
            transparent,
            rgba(80, 120, 210, 0.35)
          );
        }

        /* RESPONSIVE */

        @media (max-width: 1100px) {
          .camera-card {
  width: 100%;
}

.hero-content {
  width: 100%;
}

          .feature-row {
            gap: 9px;
          }

          .feature-divider {
            display: none;
          }
        }

        @media (max-width: 850px) {
          .topbar {
            padding: 0 18px;
          }

          .signature {
            display: none;
          }

          .sidebar {
            width: 75px;
            padding: 22px 9px;
          }

          .sidebar-label,
          .nav-item span,
          .mini-card,
          .side-decoration {
            display: none;
          }

          .nav-item {
            justify-content: center;
            padding: 14px;
          }

          .active-arrow {
            display: none;
          }

          .content {
            padding: 20px 15px;
          }

          .hero {
            min-height: 390px;
          }

          .hero-content {
            width: 100%;
            padding: 35px 25px;
          }

          .camera-card {
  position: relative;
  top: auto;
  left: auto;
  right: auto;
  width: 100%;
  min-width: 0;
}

          .lower-grid {
            grid-template-columns: 1fr;
          }
        }

        @media (max-width: 600px) {
          .brand-subtitle {
            display: none;
          }

          .brand-name {
            font-size: 18px;
          }

          .system-status {
            font-size: 10px;
            padding: 8px 11px;
          }

          .hero h1 {
            font-size: 37px;
          }

          .feature-row {
            flex-wrap: wrap;
          }

          .stats-grid {
            grid-template-columns: 1fr;
          }

           .camera-card {
  top: auto;
}
        }
      `}</style>
    </div>
  );
}

export default App;