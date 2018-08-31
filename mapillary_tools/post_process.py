import os
import sys
import processing
import uploader


def post_process(import_path,
                 video_file=None,
                 summarize=False,
                 filter_out_duplicates=False,
                 save_as_json=False,
                 list_file_status=False,
                 push_images=False,
                 master_upload=False,
                 skip_subfolders=False):

    # sanity check if video file is passed
    if video_file and not (os.path.isdir(video_file) or os.path.isfile(video_file)):
        print("Error, video path " + video_file +
              " does not exist, exiting...")
        sys.exit(1)

    # in case of video processing, adjust the import path
    if video_file:
        # set sampling path
        video_sampling_path = processing.sampled_video_frames_rootpath(
            video_file)
        import_path = os.path.join(os.path.abspath(import_path), video_sampling_path) if import_path else os.path.join(
            os.path.dirname(video_file), video_sampling_path)

    # basic check for all
    if not import_path or not os.path.isdir(import_path):
        print("Error, import directory " + import_path +
              " does not exist, exiting...")
        sys.exit(1)

    summary_dict = {}
    status_list_dict = {}

    total_files = len(uploader.get_total_file_list(import_path))

    # upload
    uploaded_files = uploader.get_success_upload_file_list(
        import_path, skip_subfolders)
    uploaded_files_count = len(uploaded_files)

    failed_upload_files = uploader.get_failed_upload_file_list(
        import_path, skip_subfolders)
    failed_upload_files_count = len(failed_upload_files)

    to_be_finalized_files = uploader.get_finalize_file_list(import_path)
    to_be_finalized_files_count = len(to_be_finalized_files)

    summary_dict["total images"] = total_files
    summary_dict["upload summary"] = {
        "successfully uploaded": uploaded_files_count,
        "failed uploads": failed_upload_files_count,
        "uploaded to be finalized": to_be_finalized_files_count
    }

    status_list_dict["successfully uploaded"] = uploaded_files
    status_list_dict["failed uploads"] = failed_upload_files
    status_list_dict["uploaded to be finalized"] = to_be_finalized_files

    summary_dict["process summary"] = {}
    process_steps = ["user_process", "import_meta_process", "geotag_process",
                     "sequence_process", "upload_params_process", "mapillary_image_description"]
    process_status = ["success", "failed"]
    for step in process_steps:

        process_success = len(processing.get_process_status_file_list(
            import_path, step, "success", skip_subfolders))
        process_failed = len(processing.get_process_status_file_list(
            import_path, step, "failed", skip_subfolders))

        summary_dict["process summary"][step] = {
            "failed": process_failed,
            "success": process_success
        }

    duplicates_file_list = processing.get_duplicate_file_list(
        import_path, skip_subfolders)
    duplicates_file_list_count = len(duplicates_file_list)

    summary_dict["process summary"]["duplicates"] = duplicates_file_list_count
    status_list_dict["duplicates"] = duplicates_file_list

    if summarize:
        print("\n")
        print("import summary for import path {}".format(import_path))
        print(json.dumps(summary_dict, indent=4))

        if save_as_json:

            try:
                processing.save_json(summary_dict, os.path.join(
                    import_path, "mapillary_import_summary.json"))
            except Exception as e:
                print("Could not save summary into json at {}, due to {}".format(
                    os.path.join(import_path, "mapillary_import_summary.json"), e))

    if list_file_status:
        print("\n")
        print("list of file status for import path {}".format(import_path))
        print(json.dumps(status_list_dict, indent=4))

        if save_as_json:

            try:
                processing.save_json(status_list_dict, os.path.join(
                    import_path, "mapillary_import_image_status_list.json"))
            except Exception as e:
                print("Could not save image status list into json at {}, due to {}".format(
                    os.path.join(import_path, "mapillary_import_image_status_list.json"), e))