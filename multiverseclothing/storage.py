from whitenoise.storage import CompressedManifestStaticFilesStorage

class CustomWhiteNoiseStorage(CompressedManifestStaticFilesStorage):
    """
    Custom WhiteNoise storage that ignores missing source map files
    """
    def post_process(self, *args, **kwargs):
        # Skip problematic files that cause MissingFileError
        skipped_files = [
            'lib/lightbox/js/lightbox.min.map',
            'lib/owlcarousel/assets/owl.video.play.png',  # If this causes issues
        ]
        
        try:
            files = super().post_process(*args, **kwargs)
            for name, hashed_name, processed in files:
                if name not in skipped_files:
                    yield name, hashed_name, processed
        except Exception as e:
            # Log the error but continue processing
            print(f"Warning: Error processing static files: {e}")
            # Return original files without compression if post-processing fails
            for name in self.files:
                if name not in skipped_files:
                    yield name, name, False